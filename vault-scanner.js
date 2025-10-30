const fs = require('fs');
const path = require('path');

class VaultScanner {
  constructor(vaultRootPath) {
    this.vaultRoot = vaultRootPath;
    this.vaults = [
      { name: 'Study', path: 'Study.vault', icon: '📚', color: '#4A90E2' },
      { name: 'Creative-Incubator', path: 'Creative-Incubator.vault', icon: '🎨', color: '#E24A90' },
      { name: 'Business-Incubator', path: 'Business-Incubator.vault', icon: '💼', color: '#90E24A' },
      { name: 'Red-White', path: 'Red-White.vault', icon: '📖', color: '#E2904A' },
      { name: 'ThistleRidgeHall', path: 'ThistleRidgeHall.vault', icon: '🎯', color: '#9B59B6' },
      { name: 'SickRabbit', path: 'SickRabbit.vault', icon: '🐰', color: '#E74C3C' },
      { name: 'Library', path: 'Library.vault', icon: '📋', color: '#3498DB' },
      { name: 'Life-Systems', path: 'Life-Systems.vault', icon: '⚙️', color: '#2ECC71' }
    ];
  }

  /**
   * Count markdown files in a directory recursively
   */
  countMarkdownFiles(dirPath) {
    let count = 0;
    try {
      const items = fs.readdirSync(dirPath, { withFileTypes: true });

      for (const item of items) {
        const fullPath = path.join(dirPath, item.name);

        if (item.isDirectory()) {
          // Skip hidden directories and system folders
          if (!item.name.startsWith('.') && item.name !== 'node_modules') {
            count += this.countMarkdownFiles(fullPath);
          }
        } else if (item.isFile() && item.name.endsWith('.md')) {
          count++;
        }
      }
    } catch (error) {
      // Directory doesn't exist or can't be read
      console.error(`Error reading directory ${dirPath}:`, error.message);
    }

    return count;
  }

  /**
   * Get recently modified files in a directory
   */
  getRecentFiles(dirPath, limit = 5) {
    const files = [];

    try {
      const items = fs.readdirSync(dirPath, { withFileTypes: true });

      for (const item of items) {
        const fullPath = path.join(dirPath, item.name);

        if (item.isDirectory()) {
          if (!item.name.startsWith('.') && item.name !== 'node_modules') {
            files.push(...this.getRecentFiles(fullPath, limit * 2));
          }
        } else if (item.isFile() && item.name.endsWith('.md')) {
          const stats = fs.statSync(fullPath);
          files.push({
            name: item.name,
            path: fullPath,
            modified: stats.mtime
          });
        }
      }
    } catch (error) {
      console.error(`Error reading directory ${dirPath}:`, error.message);
    }

    // Sort by modified date and return top N
    return files
      .sort((a, b) => b.modified - a.modified)
      .slice(0, limit);
  }

  /**
   * Get folder structure and counts
   */
  getFolderStats(dirPath) {
    const folders = [];

    try {
      const items = fs.readdirSync(dirPath, { withFileTypes: true });

      for (const item of items) {
        if (item.isDirectory() && !item.name.startsWith('.') && item.name !== 'node_modules') {
          const fullPath = path.join(dirPath, item.name);
          const fileCount = this.countMarkdownFiles(fullPath);

          if (fileCount > 0) {
            folders.push({
              name: item.name,
              fileCount: fileCount
            });
          }
        }
      }
    } catch (error) {
      console.error(`Error reading directory ${dirPath}:`, error.message);
    }

    return folders.sort((a, b) => b.fileCount - a.fileCount);
  }

  /**
   * Scan all vaults and return statistics
   */
  scanAllVaults() {
    const results = [];

    for (const vault of this.vaults) {
      const vaultPath = path.join(this.vaultRoot, vault.path);

      // Check if vault exists
      if (!fs.existsSync(vaultPath)) {
        results.push({
          ...vault,
          exists: false,
          fileCount: 0,
          recentFiles: [],
          topFolders: []
        });
        continue;
      }

      const fileCount = this.countMarkdownFiles(vaultPath);
      const recentFiles = this.getRecentFiles(vaultPath, 5);
      const topFolders = this.getFolderStats(vaultPath).slice(0, 5);

      results.push({
        ...vault,
        exists: true,
        fileCount: fileCount,
        recentFiles: recentFiles.map(f => ({
          name: f.name,
          relativePath: path.relative(vaultPath, f.path),
          modified: f.modified.toISOString()
        })),
        topFolders: topFolders
      });
    }

    return results;
  }

  /**
   * Search across all vaults
   */
  searchAllVaults(query) {
    const results = [];
    const searchTerm = query.toLowerCase();

    for (const vault of this.vaults) {
      const vaultPath = path.join(this.vaultRoot, vault.path);

      if (!fs.existsSync(vaultPath)) continue;

      const matches = this.searchInDirectory(vaultPath, vaultPath, searchTerm);

      if (matches.length > 0) {
        results.push({
          vault: vault.name,
          icon: vault.icon,
          matches: matches
        });
      }
    }

    return results;
  }

  /**
   * Search in a directory recursively
   */
  searchInDirectory(dirPath, vaultRoot, searchTerm, maxResults = 20) {
    const matches = [];

    try {
      const items = fs.readdirSync(dirPath, { withFileTypes: true });

      for (const item of items) {
        if (matches.length >= maxResults) break;

        const fullPath = path.join(dirPath, item.name);

        if (item.isDirectory()) {
          if (!item.name.startsWith('.') && item.name !== 'node_modules') {
            matches.push(...this.searchInDirectory(fullPath, vaultRoot, searchTerm, maxResults - matches.length));
          }
        } else if (item.isFile() && item.name.endsWith('.md')) {
          // Check filename
          if (item.name.toLowerCase().includes(searchTerm)) {
            matches.push({
              name: item.name,
              path: path.relative(vaultRoot, fullPath),
              matchType: 'filename'
            });
          } else {
            // Check content
            try {
              const content = fs.readFileSync(fullPath, 'utf8');
              if (content.toLowerCase().includes(searchTerm)) {
                matches.push({
                  name: item.name,
                  path: path.relative(vaultRoot, fullPath),
                  matchType: 'content'
                });
              }
            } catch (error) {
              // Skip files that can't be read
            }
          }
        }
      }
    } catch (error) {
      console.error(`Error searching directory ${dirPath}:`, error.message);
    }

    return matches;
  }

  /**
   * Get deep content from a specific folder or vault
   * Returns file list with actual content for AI context
   */
  getDeepFolderContent(dirPath, maxFiles = 20, maxCharsPerFile = 3000) {
    const filesWithContent = [];

    try {
      const items = fs.readdirSync(dirPath, { withFileTypes: true });

      for (const item of items) {
        if (filesWithContent.length >= maxFiles) break;

        const fullPath = path.join(dirPath, item.name);

        if (item.isDirectory()) {
          if (!item.name.startsWith('.') && item.name !== 'node_modules') {
            filesWithContent.push(...this.getDeepFolderContent(fullPath, maxFiles - filesWithContent.length, maxCharsPerFile));
          }
        } else if (item.isFile() && item.name.endsWith('.md')) {
          try {
            const stats = fs.statSync(fullPath);
            let content = fs.readFileSync(fullPath, 'utf8');

            // Truncate if too long
            if (content.length > maxCharsPerFile) {
              content = content.substring(0, maxCharsPerFile) + '\n\n[... truncated ...]';
            }

            filesWithContent.push({
              name: item.name,
              path: path.relative(this.vaultRoot, fullPath),
              modified: stats.mtime.toISOString(),
              content: content,
              size: stats.size
            });
          } catch (error) {
            // Skip files that can't be read
            console.error(`Error reading file ${fullPath}:`, error.message);
          }
        }
      }
    } catch (error) {
      console.error(`Error reading directory ${dirPath}:`, error.message);
    }

    return filesWithContent;
  }

  /**
   * Get comprehensive file sampling from vault
   * Intelligently samples files from across all folders proportionally
   */
  getSmartVaultSample(vaultPath, maxFiles = 40) {
    const filesWithContent = [];
    const folderFiles = new Map(); // Track files per folder

    // First pass: collect all files organized by folder
    const collectFiles = (dirPath, relativeTo) => {
      try {
        const items = fs.readdirSync(dirPath, { withFileTypes: true });

        for (const item of items) {
          const fullPath = path.join(dirPath, item.name);

          if (item.isDirectory()) {
            if (!item.name.startsWith('.') && item.name !== 'node_modules') {
              collectFiles(fullPath, relativeTo);
            }
          } else if (item.isFile() && item.name.endsWith('.md')) {
            const relPath = path.relative(relativeTo, fullPath);
            const folderName = path.dirname(relPath);

            if (!folderFiles.has(folderName)) {
              folderFiles.set(folderName, []);
            }

            try {
              const stats = fs.statSync(fullPath);
              folderFiles.get(folderName).push({
                name: item.name,
                fullPath: fullPath,
                relativePath: relPath,
                modified: stats.mtime,
                size: stats.size
              });
            } catch (error) {
              // Skip files that can't be read
            }
          }
        }
      } catch (error) {
        console.error(`Error collecting files from ${dirPath}:`, error.message);
      }
    };

    collectFiles(vaultPath, vaultPath);

    // Second pass: smart sampling from each folder
    const folders = Array.from(folderFiles.entries());
    const filesPerFolder = Math.ceil(maxFiles / folders.length);

    for (const [folderName, files] of folders) {
      if (filesWithContent.length >= maxFiles) break;

      // Sort by modification date (most recent first)
      const sortedFiles = files.sort((a, b) => b.modified - a.modified);

      // Take up to filesPerFolder from this folder
      const sampled = sortedFiles.slice(0, Math.min(filesPerFolder, maxFiles - filesWithContent.length));

      for (const file of sampled) {
        try {
          let content = fs.readFileSync(file.fullPath, 'utf8');

          // Truncate if too long
          const maxChars = 3000;
          if (content.length > maxChars) {
            content = content.substring(0, maxChars) + '\n\n[... truncated ...]';
          }

          filesWithContent.push({
            name: file.name,
            path: file.relativePath,
            folder: folderName,
            modified: file.modified.toISOString(),
            content: content,
            size: file.size
          });
        } catch (error) {
          console.error(`Error reading file ${file.fullPath}:`, error.message);
        }
      }
    }

    return filesWithContent;
  }

  /**
   * Get enhanced vault context with comprehensive file sampling
   * No keyword detection - just loads representative sample from entire vault
   */
  getEnhancedVaultContext(vaultName, question = '', maxFiles = 40) {
    const vault = this.vaults.find(v => v.name.toLowerCase() === vaultName.toLowerCase());
    if (!vault) return null;

    const vaultPath = path.join(this.vaultRoot, vault.path);
    if (!fs.existsSync(vaultPath)) return null;

    // Get basic vault info
    const fileCount = this.countMarkdownFiles(vaultPath);
    const topFolders = this.getFolderStats(vaultPath).slice(0, 10);

    // Get smart sample of files from across the vault
    const filesWithContent = this.getSmartVaultSample(vaultPath, maxFiles);

    // Group files by folder for better context presentation
    const filesByFolder = {};
    filesWithContent.forEach(file => {
      const folder = file.folder || 'root';
      if (!filesByFolder[folder]) {
        filesByFolder[folder] = [];
      }
      filesByFolder[folder].push(file);
    });

    return {
      vaultName: vault.name,
      icon: vault.icon,
      fileCount: fileCount,
      topFolders: topFolders,
      filesWithContent: filesWithContent,
      filesByFolder: filesByFolder,
      totalContentFiles: filesWithContent.length,
      foldersRepresented: Object.keys(filesByFolder).length
    };
  }

  /**
   * Get enhanced context for all vaults with selective deep content
   */
  getEnhancedAllVaultsContext(question = '', maxFilesPerVault = 10) {
    const results = [];

    for (const vault of this.vaults) {
      const vaultPath = path.join(this.vaultRoot, vault.path);
      if (!fs.existsSync(vaultPath)) continue;

      const fileCount = this.countMarkdownFiles(vaultPath);
      const topFolders = this.getFolderStats(vaultPath).slice(0, 3);

      // Get recent files with content for each vault
      const recentFiles = this.getRecentFiles(vaultPath, maxFilesPerVault);
      const filesWithContent = recentFiles.map(f => {
        try {
          let content = fs.readFileSync(f.path, 'utf8');
          if (content.length > 2000) {
            content = content.substring(0, 2000) + '\n\n[... truncated ...]';
          }
          return {
            name: f.name,
            path: path.relative(vaultPath, f.path),
            content: content
          };
        } catch (error) {
          return null;
        }
      }).filter(f => f !== null);

      results.push({
        name: vault.name,
        icon: vault.icon,
        fileCount: fileCount,
        topFolders: topFolders,
        recentFilesWithContent: filesWithContent.slice(0, 5)
      });
    }

    return results;
  }

  /**
   * Get active projects across all vaults
   * Projects are identified by:
   * 1. PROJECT-STATUS.md or PROJECT-OVERVIEW.md files
   * 2. Vaults themselves (as fallback for active vaults)
   */
  getActiveProjects() {
    const projects = [];

    // Scan for PROJECT-STATUS.md files
    for (const vault of this.vaults) {
      const vaultPath = path.join(this.vaultRoot, vault.path);
      if (!fs.existsSync(vaultPath)) continue;

      // Look for project files in vault root and subdirectories
      const projectFiles = this.findProjectFiles(vaultPath, vault);
      projects.push(...projectFiles);
    }

    // If we found project files, return them
    if (projects.length > 0) {
      // Sort by priority: in-progress > pending > completed
      const priorityMap = { 'in-progress': 1, 'active': 1, 'pending': 2, 'completed': 3, 'on-hold': 4 };
      projects.sort((a, b) => {
        const aPriority = priorityMap[a.status.toLowerCase()] || 5;
        const bPriority = priorityMap[b.status.toLowerCase()] || 5;
        return aPriority - bPriority;
      });
      return projects.slice(0, 5); // Return top 5 projects
    }

    // Fallback: treat active vaults as projects
    const vaultProjects = this.scanAllVaults()
      .filter(v => v.exists && v.fileCount > 0)
      .map(v => ({
        name: v.name,
        vault: v.name,
        icon: v.icon,
        status: v.fileCount > 50 ? 'Active' : 'Pending',
        progress: Math.min(Math.floor((v.fileCount / 500) * 100), 100), // Estimate based on file count
        deadline: null,
        fileCount: v.fileCount,
        lastUpdated: v.recentFiles[0]?.modified || new Date().toISOString()
      }));

    return vaultProjects.slice(0, 5);
  }

  /**
   * Find PROJECT-STATUS.md or PROJECT-OVERVIEW.md files in a vault
   */
  findProjectFiles(dirPath, vault, depth = 0, maxDepth = 2) {
    const projects = [];
    if (depth > maxDepth) return projects;

    try {
      const items = fs.readdirSync(dirPath, { withFileTypes: true });

      for (const item of items) {
        const fullPath = path.join(dirPath, item.name);

        if (item.isDirectory()) {
          if (!item.name.startsWith('.') && item.name !== 'node_modules') {
            projects.push(...this.findProjectFiles(fullPath, vault, depth + 1, maxDepth));
          }
        } else if (item.isFile() &&
                   (item.name === 'PROJECT-STATUS.md' ||
                    item.name === 'PROJECT-OVERVIEW.md' ||
                    item.name.match(/^PROJECT.*\.md$/i))) {
          const projectInfo = this.parseProjectFile(fullPath, vault);
          if (projectInfo) {
            projects.push(projectInfo);
          }
        }
      }
    } catch (error) {
      console.error(`Error finding project files in ${dirPath}:`, error.message);
    }

    return projects;
  }

  /**
   * Parse a PROJECT-STATUS.md file to extract project metadata
   */
  parseProjectFile(filePath, vault) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const stats = fs.statSync(filePath);

      // Extract project name from heading or file location
      const nameMatch = content.match(/^#\s+(.+?)$/m);
      const projectName = nameMatch ? nameMatch[1].trim() : path.basename(path.dirname(filePath));

      // Extract status
      const statusMatch = content.match(/status[:\s]+([^\n]+)/i);
      const status = statusMatch ? statusMatch[1].trim() : 'In Progress';

      // Extract deadline
      const deadlineMatch = content.match(/deadline[:\s]+([^\n]+)/i);
      const deadline = deadlineMatch ? deadlineMatch[1].trim() : null;

      // Estimate progress from phase completion markers
      let progress = 50; // Default
      const phaseMatches = content.match(/phase\s+\d+.*?(\d+)%/gi);
      if (phaseMatches && phaseMatches.length > 0) {
        const percentages = phaseMatches.map(m => parseInt(m.match(/(\d+)%/)[1]));
        progress = Math.floor(percentages.reduce((a, b) => a + b, 0) / percentages.length);
      } else if (content.match(/complete|done|finished/i)) {
        progress = 100;
      } else if (content.match(/started|in progress|ongoing/i)) {
        progress = 50;
      }

      return {
        name: projectName.replace(/project/i, '').trim() || vault.name,
        vault: vault.name,
        icon: vault.icon,
        status: status,
        progress: Math.min(progress, 100),
        deadline: deadline,
        filePath: path.relative(this.vaultRoot, filePath),
        lastUpdated: stats.mtime.toISOString()
      };
    } catch (error) {
      console.error(`Error parsing project file ${filePath}:`, error.message);
      return null;
    }
  }
}

module.exports = VaultScanner;
