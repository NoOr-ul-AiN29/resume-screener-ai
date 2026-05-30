// server.js — Express replacement for FastAPI app.py
const express = require('express');
const multer  = require('multer');
const pdfParse = require('pdf-parse');
const path = require('path');

const { extractSkillsFromText, extractSkillsFromJobDescription } = require('./parser');
const { calculateMatch } = require('./matcher');

const app  = express();
const PORT = process.env.PORT || 3000;

// ── Middleware ─────────────────────────────────────────────────────────────
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// multer — store PDF in memory (no disk needed)
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 20 * 1024 * 1024 }, // 20MB
  fileFilter: (req, file, cb) => {
    if (file.mimetype === 'application/pdf' || file.originalname.toLowerCase().endsWith('.pdf')) {
      cb(null, true);
    } else {
      cb(new Error('Only PDF files are accepted.'));
    }
  }
});

// ── Routes ─────────────────────────────────────────────────────────────────

// Serve frontend
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// POST /screen — main endpoint
app.post('/screen', upload.single('resume'), async (req, res) => {
  try {
    // Validate file
    if (!req.file) {
      return res.status(400).json({ detail: 'No resume file uploaded. Please upload a PDF.' });
    }

    // Validate job description
    const jobDescription = (req.body.job_description || '').trim();
    if (!jobDescription) {
      return res.status(400).json({ detail: 'Job description cannot be empty.' });
    }

    // Extract text from PDF buffer (no disk write needed)
    let resumeText;
    try {
      const pdfData = await pdfParse(req.file.buffer);
      resumeText = pdfData.text;
    } catch (e) {
      return res.status(422).json({ detail: 'Failed to read PDF. The file may be corrupted or image-only.' });
    }

    if (!resumeText || !resumeText.trim()) {
      return res.status(422).json({ detail: 'No readable text found in the PDF. It may contain only scanned images.' });
    }

    // Extract skills
    const resumeSkills = extractSkillsFromText(resumeText);
    const jobSkills    = extractSkillsFromJobDescription(jobDescription);

    // Calculate match
    const result = calculateMatch(resumeSkills, jobSkills);

    return res.json(result);

  } catch (err) {
    console.error('[server] Error:', err.message);
    return res.status(500).json({ detail: err.message || 'Internal server error.' });
  }
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Resume Screener AI is running.' });
});

// ── Start ──────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`[server] Resume Screener AI running on http://localhost:${PORT}`);
});