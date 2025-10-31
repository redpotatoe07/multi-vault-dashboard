const express = require('express');
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');
const VaultScanner = require('./vault-scanner');
const RAGClient = require('./rag-client');
const fetch = require('node-fetch');

const execAsync = promisify(exec);
const app = express();
const PORT = 3000;
const OLLAMA_SERVICE_URL = 'http://localhost:5000';
const RAG_SERVICE_URL = 'http://localhost:5001';

// Middleware to parse JSON bodies
app.use(express.json());

// Configuration - UPDATE THIS PATH TO YOUR VAULT LOCATION
const VAULT_ROOT = 'C:\\Users\\redpo\\repos\\Obsidian\\Multi-Vault';

// Initialize vault scanner
const scanner = new VaultScanner(VAULT_ROOT);

// Initialize RAG client
const ragClient = new RAGClient(RAG_SERVICE_URL);

// Serve static files
app.use(express.static('public'));

// API endpoint: Get all vault statistics
app.get('/api/vaults', (req, res) => {
  try {
    const vaultData = scanner.scanAllVaults();
    res.json({
      success: true,
      vaultRoot: VAULT_ROOT,
      vaults: vaultData,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// API endpoint: Get active projects
app.get('/api/projects', (req, res) => {
  try {
    const projects = scanner.getActiveProjects();
    res.json({
      success: true,
      projects: projects,
      count: projects.length,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// API endpoint: Get recent activity across all vaults
app.get('/api/recent-activity', (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 10;
    const activity = scanner.getRecentActivity(limit);
    res.json({
      success: true,
      activity: activity,
      count: activity.length,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// API endpoint: Get detailed project information
app.get('/api/project/:identifier', (req, res) => {
  try {
    const identifier = req.params.identifier;
    const type = req.query.type || 'name'; // 'name' or 'vault'

    const projectDetails = scanner.getProjectDetails(identifier, type);

    if (projectDetails) {
      res.json({
        success: true,
        project: projectDetails,
        timestamp: new Date().toISOString()
      });
    } else {
      res.status(404).json({
        success: false,
        error: `Project not found: ${identifier}`
      });
    }
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// API endpoint: Search across all vaults (using RAG hybrid search)
app.get('/api/search', async (req, res) => {
  const query = req.query.q;
  const vault = req.query.vault || 'all'; // Support vault filtering

  if (!query || query.trim().length === 0) {
    return res.json({
      success: false,
      error: 'Search query is required'
    });
  }

  try {
    // If searching all vaults, search each vault and combine results
    if (vault === 'all') {
      const vaultNames = ['Study', 'Creative-Incubator', 'Business-Incubator', 'Red-White', 'ThistleRidgeHall', 'SickRabbit', 'Library', 'Life-Systems', 'Praxis'];
      const allResults = [];

      // Search each vault in parallel
      const searchPromises = vaultNames.map(async (vaultName) => {
        try {
          const response = await fetch(`${RAG_SERVICE_URL}/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              vault_name: vaultName,
              query: query.trim(),
              limit: 5 // Get top 5 from each vault
            })
          });
          const data = await response.json();

          // Add vault name to each result
          if (data.results) {
            return data.results.map(result => ({
              ...result,
              vault: vaultName
            }));
          }
          return [];
        } catch (error) {
          console.error(`Error searching ${vaultName}:`, error);
          return [];
        }
      });

      const resultsArrays = await Promise.all(searchPromises);
      const combinedResults = resultsArrays.flat();

      // Sort by score (lower distance = better match)
      combinedResults.sort((a, b) => a.distance - b.distance);

      res.json({
        success: true,
        query: query,
        vault: 'all',
        result_count: combinedResults.length,
        results: combinedResults.slice(0, 20), // Return top 20 overall
        timestamp: new Date().toISOString()
      });
    } else {
      // Search specific vault
      const response = await fetch(`${RAG_SERVICE_URL}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          vault_name: vault,
          query: query.trim(),
          limit: 20
        })
      });

      const data = await response.json();

      res.json({
        success: true,
        query: query,
        vault: vault,
        query_type: data.query_type,
        search_strategy: data.search_strategy,
        result_count: data.result_count,
        results: data.results,
        timestamp: new Date().toISOString()
      });
    }
  } catch (error) {
    console.error('Search error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// API endpoint: Health check
app.get('/api/health', (req, res) => {
  res.json({
    success: true,
    status: 'running',
    vaultRoot: VAULT_ROOT,
    timestamp: new Date().toISOString()
  });
});

// API endpoint: Check if Ollama is available (via Python service)
app.get('/api/ollama/status', async (req, res) => {
  try {
    // Check Python service health
    const response = await fetch(`${OLLAMA_SERVICE_URL}/health`, { timeout: 5000 });
    const data = await response.json();

    if (response.ok && data.ollama === 'connected') {
      res.json({
        success: true,
        available: true,
        message: 'Ollama Python service is running',
        service: 'python-sdk'
      });
    } else {
      res.json({
        success: true,
        available: false,
        message: data.message || 'Ollama service not available',
        service: 'python-sdk'
      });
    }
  } catch (error) {
    res.json({
      success: true,
      available: false,
      message: 'Ollama Python service not running. Start it with: cd ollama-service && python app.py',
      service: 'python-sdk',
      error: error.message
    });
  }
});

// API endpoint: Check if Claude Code is available
app.get('/api/claude/status', async (req, res) => {
  try {
    // Check if claude command exists
    await execAsync('claude --version', { timeout: 5000 });
    res.json({
      success: true,
      available: true,
      message: 'Claude Code is available'
    });
  } catch (error) {
    res.json({
      success: true,
      available: false,
      message: 'Claude Code not found'
    });
  }
});

// API endpoint: Check if RAG service is available
app.get('/api/rag/status', async (req, res) => {
  try {
    const health = await ragClient.healthCheck();

    if (health.status === 'healthy') {
      // Get collections info
      const collections = await ragClient.getCollections();

      res.json({
        success: true,
        available: true,
        message: 'RAG service is running',
        version: health.version,
        collections: collections.collections || [],
        total_documents: collections.collections
          ? collections.collections.reduce((sum, c) => sum + c.document_count, 0)
          : 0
      });
    } else {
      res.json({
        success: true,
        available: false,
        message: 'RAG service not available',
        error: health.error
      });
    }
  } catch (error) {
    res.json({
      success: true,
      available: false,
      message: 'RAG service not running. Start it with: cd rag-service && python app.py',
      error: error.message
    });
  }
});

// API endpoint: Ask Ollama a question about vaults (NEW - using Python service with streaming)
app.post('/api/ollama/ask', async (req, res) => {
  const { question, vault } = req.body;

  if (!question || question.trim().length === 0) {
    return res.status(400).json({
      success: false,
      error: 'Question is required'
    });
  }

  try {
    // DEBUG: Log what we received
    console.log('\n=== OLLAMA REQUEST DEBUG ===');
    console.log('Question:', question);
    console.log('Vault selected:', vault);

    // Build vault path
    let vaultPath = VAULT_ROOT;
    if (vault && vault !== 'all') {
      const vaultConfig = scanner.vaults.find(v => v.name === vault);
      console.log('Vault config found:', vaultConfig);
      if (vaultConfig) {
        vaultPath = path.join(VAULT_ROOT, vaultConfig.path);
        console.log('Vault path:', vaultPath);
      }
    }

    // Get file content using RAG hybrid search
    let fileContent = '';
    if (vault && vault !== 'all') {
      // Use RAG hybrid search to find relevant files
      try {
        console.log('Using RAG hybrid search to find relevant files...');

        // Search using RAG service
        const ragResults = await ragClient.search(vault, question, true);

        if (ragResults && !ragResults.error && ragResults.results && ragResults.results.length > 0) {
          console.log(`[RAG] Found ${ragResults.result_count} files`);
          console.log(`[RAG] Query type: ${ragResults.query_type}, Strategy: ${ragResults.search_strategy}`);
          console.log('[RAG] Top 3 matches:');
          ragResults.results.slice(0, 3).forEach((result, i) => {
            const filename = result.metadata?.filename || 'Unknown';
            const score = result.score || 0;
            console.log(`   ${i+1}. ${filename} (score: ${score.toFixed(3)})`);
          });

          // For LIST_ALL queries, return RAG results directly without LLM processing
          // This prevents hallucinations and is much faster
          if (ragResults.query_type === 'list_all') {
            console.log('[RAG] Detected list_all query - returning results directly (no LLM)');

            const itemList = ragResults.results.map(result => {
              const filename = result.metadata?.filename || 'Unknown';
              const path = result.metadata?.file_path || '';
              // Remove .md extension for cleaner display
              const displayName = filename.replace(/\.md$/, '');
              return `• ${displayName}`;
            }).join('\n');

            const entity = ragResults.routing?.entity || 'items';
            const answer = `Based on the vault files, here is a list of ${entity} in ${vault}:\n\n${itemList}\n\nTotal: ${ragResults.result_count} ${entity} found.`;

            return res.json({
              success: true,
              question: question,
              answer: answer,
              vault: vault,
              model: 'rag-direct',
              query_type: ragResults.query_type,
              search_strategy: ragResults.search_strategy,
              result_count: ragResults.result_count,
              timestamp: new Date().toISOString()
            });
          }

          // Format results for Ollama
          const relevantFiles = ragResults.results.map(result => ({
            name: result.metadata?.filename || 'Unknown',
            path: result.metadata?.file_path || '',
            content: result.document || '',
            score: result.score || 0
          }));

          console.log(`[RAG] Using ${relevantFiles.length} files for context`);

          // Format file content
          if (relevantFiles.length > 15) {
            fileContent = `The vault contains ${relevantFiles.length} relevant files for your query.\n\n`;
            fileContent += relevantFiles.map(f =>
              `--- FILE: ${f.name} (relevance: ${f.score.toFixed(3)}) ---\nPath: ${f.path}\n\n${f.content}\n\n`
            ).join('');
          } else {
            fileContent = relevantFiles.map(f =>
              `--- FILE: ${f.name} (relevance: ${f.score.toFixed(3)}) ---\nPath: ${f.path}\n\n${f.content}\n\n`
            ).join('');
          }
          console.log('Total file content length:', fileContent.length, 'characters');
        } else {
          console.log('[WARNING] RAG search returned no results, falling back to smart sampling');
          throw new Error('No RAG search results');
        }
      } catch (err) {
        // Fallback to original smart sampling if RAG search fails
        console.log('[INFO] Using fallback: smart vault sampling');
        console.log('[ERROR]', err.message);
        const vaultData = scanner.getSmartVaultSample(vaultPath, 30);
        console.log('Files loaded from vault:', vaultData.length);
        console.log('Sample files:', vaultData.slice(0, 3).map(f => f.name));
        fileContent = vaultData.map(f =>
          `--- FILE: ${f.name} ---\nPath: ${f.path}\n\n${f.content}\n\n`
        ).join('');
        console.log('Total file content length:', fileContent.length, 'characters');
      }
    } else {
      const allVaultsData = scanner.getEnhancedAllVaultsContext(question, 5);
      fileContent = allVaultsData.map(v =>
        `=== VAULT: ${v.icon} ${v.name} ===\n\n` +
        v.recentFilesWithContent.map(f =>
          `--- FILE: ${f.name} ---\n${f.content}\n\n`
        ).join('')
      ).join('\n\n');
    }

    // Build messages for Ollama - put file content in user message for better context handling
    const messages = [
      {
        role: 'system',
        content: 'You are a helpful assistant that answers questions about Obsidian vault files. You will be given file contents followed by a question. Answer based ONLY on the provided files.'
      },
      {
        role: 'user',
        content: `Here are the files from the vault:

${fileContent}

---
Question: ${question}

Please answer based only on the files above. Reference specific file names and details.`
      }
    ];

    // Log a preview to verify
    console.log('System message length:', messages[0].content.length, 'chars');
    console.log('Question:', question);

    // Call Python service with streaming (using llama3.2:3b for better instruction following)
    const pythonResponse = await fetch(`${OLLAMA_SERVICE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: messages,
        model: 'llama3.2:3b',  // Changed from gemma3 - better at following context instructions
        stream: true
      })
    });

    if (!pythonResponse.ok) {
      const error = await pythonResponse.json();
      return res.status(500).json({
        success: false,
        error: error.error || 'Failed to get response from Ollama service'
      });
    }

    // Set up Server-Sent Events (SSE) for streaming
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    // Stream the response from Python service to client
    pythonResponse.body.on('data', (chunk) => {
      res.write(chunk);
    });

    pythonResponse.body.on('end', () => {
      res.end();
    });

    pythonResponse.body.on('error', (error) => {
      console.error('Stream error:', error);
      res.end();
    });

  } catch (error) {
    console.error('Ollama error:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to get response from Ollama'
    });
  }
});

// API endpoint: Ask Claude Code a question about vaults
app.post('/api/claude/ask', async (req, res) => {
  const { question, vault } = req.body;

  if (!question || question.trim().length === 0) {
    return res.status(400).json({
      success: false,
      error: 'Question is required'
    });
  }

  try {
    // Check if Claude Code is available
    try {
      await execAsync('claude --version', { timeout: 5000 });
    } catch (error) {
      return res.status(503).json({
        success: false,
        error: 'Claude Code is not available'
      });
    }

    // Build vault path
    let vaultPath = VAULT_ROOT;
    if (vault && vault !== 'all') {
      const vaultConfig = scanner.vaults.find(v => v.name === vault);
      if (vaultConfig) {
        vaultPath = path.join(VAULT_ROOT, vaultConfig.path);
      }
    }

    // Get file content using RAG hybrid search (same as Ollama integration)
    const fs = require('fs');
    const os = require('os');

    let fileContent = '';
    if (vault && vault !== 'all') {
      // Use RAG hybrid search to find relevant files
      try {
        console.log('[CLAUDE] Using RAG hybrid search to find relevant files...');

        // Search using RAG service
        const ragResults = await ragClient.search(vault, question, true);

        if (ragResults && !ragResults.error && ragResults.results && ragResults.results.length > 0) {
          console.log(`[CLAUDE-RAG] Found ${ragResults.result_count} files`);
          console.log(`[CLAUDE-RAG] Query type: ${ragResults.query_type}, Strategy: ${ragResults.search_strategy}`);
          console.log('[CLAUDE-RAG] Top 3 matches:');
          ragResults.results.slice(0, 3).forEach((result, i) => {
            const filename = result.metadata?.filename || 'Unknown';
            const score = result.score || 0;
            console.log(`   ${i+1}. ${filename} (score: ${score.toFixed(3)})`);
          });

          // Format results for Claude
          const relevantFiles = ragResults.results.map(result => ({
            name: result.metadata?.filename || 'Unknown',
            path: result.metadata?.file_path || '',
            content: result.document || '',
            score: result.score || 0
          }));

          console.log(`[CLAUDE-RAG] Using ${relevantFiles.length} files for context`);
          console.log(`[CLAUDE-RAG] Token savings: ~${(30 - relevantFiles.length) * 500} tokens (estimated)`);

          // Format file content
          fileContent = relevantFiles.map(f =>
            `--- FILE: ${f.name} (relevance: ${f.score.toFixed(3)}) ---\nPath: ${f.path}\n\n${f.content}\n\n`
          ).join('');

          console.log('[CLAUDE-RAG] Total file content length:', fileContent.length, 'characters');
        } else {
          console.log('[CLAUDE-RAG] WARNING: RAG search returned no results, falling back to smart sampling');
          throw new Error('No RAG search results');
        }
      } catch (err) {
        // Fallback to original smart sampling if RAG search fails
        console.log('[CLAUDE] Using fallback: smart vault sampling');
        console.log('[CLAUDE] ERROR:', err.message);
        const vaultData = scanner.getSmartVaultSample(vaultPath, 30);
        fileContent = vaultData.map(f =>
          `--- FILE: ${f.name} ---\nPath: ${f.path}\n\n${f.content}\n\n`
        ).join('');
        console.log('[CLAUDE] Total file content length:', fileContent.length, 'characters');
      }
    } else {
      const allVaultsData = scanner.getEnhancedAllVaultsContext(question, 5);
      fileContent = allVaultsData.map(v =>
        `=== VAULT: ${v.icon} ${v.name} ===\n\n` +
        v.recentFilesWithContent.map(f =>
          `--- FILE: ${f.name} ---\n${f.content}\n\n`
        ).join('')
      ).join('\n\n');
    }

    // Create bash script that pipes content to Claude
    const scriptPath = path.join(os.tmpdir(), `claude-${Date.now()}.sh`);
    const contentPath = path.join(os.tmpdir(), `content-${Date.now()}.txt`);

    // Write content to file
    fs.writeFileSync(contentPath, fileContent, 'utf8');

    // Create bash script with content + question
    const script = `#!/bin/bash\ncat "${contentPath.replace(/\\/g, '/')}" | claude chat "${question}"`;
    fs.writeFileSync(scriptPath, script, 'utf8');

    // Run the bash script
    const { stdout, stderr } = await execAsync(`bash "${scriptPath}"`, {
      timeout: 120000,
      maxBuffer: 1024 * 1024 * 10
    });

    // Clean up temp files
    try {
      fs.unlinkSync(scriptPath);
      fs.unlinkSync(contentPath);
    } catch (e) {
      // Ignore cleanup errors
    }

    // Filter out ANSI escape codes
    const cleanOutput = stdout.replace(/\x1B\[[0-9;?]*[a-zA-Z]/g, '').replace(/\[\?[0-9]+[hl]/g, '').trim();

    if (stderr && !stderr.includes('claude') && !stderr.includes('Using')) {
      console.error('Claude Code stderr:', stderr);
    }

    res.json({
      success: true,
      question: question,
      answer: cleanOutput,
      vault: vault || 'all',
      model: 'claude-code',
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Claude Code error:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Failed to get response from Claude Code'
    });
  }
});

// API endpoint: RAG hybrid search (single vault)
app.post('/api/rag/search', async (req, res) => {
  const { vault, query, explain } = req.body;

  if (!query || query.trim().length === 0) {
    return res.status(400).json({
      success: false,
      error: 'Query is required'
    });
  }

  if (!vault) {
    return res.status(400).json({
      success: false,
      error: 'Vault name is required'
    });
  }

  try {
    const results = await ragClient.search(vault, query, explain || false);

    if (results.error) {
      return res.status(500).json({
        success: false,
        error: results.error
      });
    }

    res.json({
      success: true,
      ...results
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// API endpoint: RAG cross-vault search
app.post('/api/rag/search-multi', async (req, res) => {
  const { vaults, query } = req.body;

  if (!query || query.trim().length === 0) {
    return res.status(400).json({
      success: false,
      error: 'Query is required'
    });
  }

  if (!vaults || !Array.isArray(vaults) || vaults.length === 0) {
    return res.status(400).json({
      success: false,
      error: 'Vaults array is required'
    });
  }

  try {
    const results = await ragClient.searchMultipleVaults(vaults, query);

    res.json({
      success: true,
      ...results
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// API endpoint: Get RAG collections
app.get('/api/rag/collections', async (req, res) => {
  try {
    const collections = await ragClient.getCollections();

    res.json({
      success: true,
      ...collections
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log('\n🚀 Multi-Vault Dashboard Started!');
  console.log('='.repeat(50));
  console.log(`📍 Vault Root: ${VAULT_ROOT}`);
  console.log(`\n🖥️  Access on this PC:`);
  console.log(`   http://localhost:${PORT}`);
  console.log(`\n📱 Access from mobile (same network):`);
  console.log(`   1. Find your PC's IP address:`);
  console.log(`      Windows: Run "ipconfig" and look for IPv4 Address`);
  console.log(`      Mac/Linux: Run "ifconfig" or "ip addr"`);
  console.log(`   2. Open this URL on your phone:`);
  console.log(`      http://YOUR_PC_IP:${PORT}`);
  console.log(`\n💡 Example: http://192.168.1.100:${PORT}`);
  console.log('='.repeat(50));
  console.log('\n✨ Dashboard is ready! Press Ctrl+C to stop.\n');
});
