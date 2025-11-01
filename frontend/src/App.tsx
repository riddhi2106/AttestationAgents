import React, { useState } from 'react'
import {
  Container,
  Typography,
  Box,
  Button,
  Paper,
  LinearProgress,
  Tooltip,
  IconButton,
  Grid,
} from '@mui/material'
import { FaMoon, FaSun } from 'react-icons/fa'

const FORBIDDEN_EXPLANATIONS: Record<string, string> = {
  'GPL-3.0': 'GPL-3.0 is copyleft; cannot be used in proprietary projects.',
  'AGPL-3.0': 'AGPL-3.0 requires server-side code sharing.',
}

const BG = { light: '#f5f5f5', dark: ' #3a3a3a' }
const CARD_BG = { light: '#ffffff', dark: '#605d5dff' } // slightly lighter than page dark
const TEXT = { light: '#121212', dark: '#f5f5f5' }

function App() {
  const [darkMode, setDarkMode] = useState(false)
  const [compliance, setCompliance] = useState(0)
  const [violations, setViolations] = useState<string[]>([])
  const [detectedLicenses, setDetectedLicenses] = useState<string[]>([])
  const [recentScans, setRecentScans] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [progressValue, setProgressValue] = useState(0)

  const toggleDarkMode = () => setDarkMode(!darkMode)
  const mode = darkMode ? 'dark' : 'light'

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setCompliance(0)
    setProgressValue(0)
    setLoading(true)

    const reader = new FileReader()
    reader.onload = async () => {
      const content = reader.result as string
      try {
        const res = await fetch('http://localhost:8000/scan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ file_name: file.name, file_content: content }),
        })
        const data = await res.json()

        setViolations(data.violations || [])
        setDetectedLicenses(data.detected || [])

        const score = data.detected.length
          ? Math.round(
              ((data.detected.length - data.violations.length) /
                data.detected.length) *
                100
            )
          : 100

        // Animate progress bar from 0 → score
        let current = 0
        const interval = setInterval(() => {
          current += 5
          if (current >= score) {
            current = score
            clearInterval(interval)
          }
          setProgressValue(current)
        }, 50)

        setCompliance(score)
        setRecentScans((prev) => [file.name, ...prev.slice(0, 4)])
      } catch (err) {
        console.error(err)
        alert('Scan failed. Make sure backend is running.')
        setProgressValue(0)
      } finally {
        setLoading(false)
      }
    }
    reader.readAsText(file)
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        bgcolor: BG[mode],
        color: TEXT[mode],
        transition: 'all 0.3s',
        p: 2,
      }}
    >
      <Container maxWidth="lg">
        {/* Header */}
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h4">Attestation Scanner</Typography>
          <IconButton onClick={toggleDarkMode}>
            {darkMode ? <FaSun /> : <FaMoon />}
          </IconButton>
        </Box>

        <Grid container spacing={2}>
          {/* Main content */}
          <Grid item xs={12} md={8}>
            {/* Scan Progress */}
            <Paper sx={{ p: 3, mb: 3, bgcolor: CARD_BG[mode], boxShadow: 3, borderRadius: 2 }}>
              <Typography variant="h6">Scan Progress</Typography>
              <LinearProgress
                variant="determinate"
                value={loading ? progressValue : compliance}
                sx={{
                  mt: 1,
                  height: 10,
                  borderRadius: 5,
                  bgcolor: darkMode ? '#2a2a2a' : '#e0e0e0',
                  '& .MuiLinearProgress-bar': {
                    bgcolor: darkMode ? '#90caf9' : '#1976d2',
                  },
                }}
              />
              <Typography sx={{ mt: 1 }}>
                {loading ? 'Scanning...' : `${compliance}% compliant`}
              </Typography>
            </Paper>

            {/* Detected Licenses */}
            <Paper sx={{ p: 3, mb: 3, bgcolor: CARD_BG[mode], boxShadow: 3, borderRadius: 2 }}>
              <Typography variant="h6">Detected Licenses</Typography>
              {detectedLicenses.length === 0 ? (
                <Typography>No licenses detected yet</Typography>
              ) : (
                detectedLicenses.map((lic) => <Typography key={lic}>{lic}</Typography>)
              )}
            </Paper>

            {/* Violations */}
            <Paper sx={{ p: 3, mb: 3, bgcolor: CARD_BG[mode], boxShadow: 3, borderRadius: 2 }}>
              <Typography variant="h6">Violations</Typography>
              {violations.length === 0 ? (
                <Typography>No forbidden licenses found ✅</Typography>
              ) : (
                violations.map((v) => (
                  <Tooltip key={v} title={FORBIDDEN_EXPLANATIONS[v] || ''}>
                    <Typography color="error">{v}</Typography>
                  </Tooltip>
                ))
              )}
            </Paper>

            {/* Upload Button */}
            <Box mt={3}>
              <Button variant="contained" component="label" disabled={loading}>
                {loading ? 'Scanning...' : 'Upload & Scan'}
                <input type="file" hidden onChange={handleFileUpload} />
              </Button>
            </Box>
          </Grid>

          {/* Recent Scans Sidebar */}
          <Grid item xs={12} md={4}>
            {recentScans.length > 0 && (
              <Paper
                sx={{
                  p: 2,
                  position: 'sticky',
                  top: 16,
                  bgcolor: darkMode ? '#3d3d3d' : '#fefefe', // lighter sidebar
                  boxShadow: 3,
                  borderRadius: 2,
                }}
              >
                <Typography variant="h6">Recent Scans</Typography>
                {recentScans.map((scan) => (
                  <Typography key={scan} sx={{ fontSize: '0.9rem' }}>
                    {scan}
                  </Typography>
                ))}
              </Paper>
            )}
          </Grid>
        </Grid>
      </Container>
    </Box>
  )
}

export default App
