/**
 * RAG Service Client
 *
 * Client module for interacting with the Python RAG service (port 5001)
 * Provides hybrid search, collections management, and indexing capabilities
 */

const fetch = require('node-fetch');

class RAGClient {
  constructor(baseURL = 'http://localhost:5001') {
    this.baseURL = baseURL;
  }

  /**
   * Check if RAG service is healthy
   */
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/health`, { timeout: 5000 });
      return await response.json();
    } catch (error) {
      return {
        status: 'unavailable',
        error: error.message
      };
    }
  }

  /**
   * Search a vault using hybrid search
   *
   * @param {string} vaultName - Name of the vault to search
   * @param {string} query - Search query
   * @param {boolean} explain - Include routing explanation
   * @returns {Promise<Object>} Search results
   */
  async search(vaultName, query, explain = false) {
    try {
      const response = await fetch(`${this.baseURL}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          vault_name: vaultName,
          query: query,
          explain: explain
        }),
        timeout: 30000
      });

      if (!response.ok) {
        throw new Error(`RAG search failed: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      return {
        error: error.message,
        query: query,
        results: [],
        result_count: 0
      };
    }
  }

  /**
   * Search across multiple vaults and aggregate results
   *
   * @param {Array<string>} vaultNames - Array of vault names to search
   * @param {string} query - Search query
   * @returns {Promise<Object>} Aggregated search results
   */
  async searchMultipleVaults(vaultNames, query) {
    try {
      // Search all vaults in parallel
      const searchPromises = vaultNames.map(vaultName =>
        this.search(vaultName, query, false)
      );

      const results = await Promise.all(searchPromises);

      // Aggregate results
      const aggregated = {
        query: query,
        vaults_searched: vaultNames.length,
        results_by_vault: {},
        all_results: [],
        total_results: 0
      };

      results.forEach((result, index) => {
        const vaultName = vaultNames[index];

        if (!result.error) {
          aggregated.results_by_vault[vaultName] = {
            query_type: result.query_type,
            search_strategy: result.search_strategy,
            result_count: result.result_count,
            results: result.results
          };

          // Add vault name to each result for tracking
          const resultsWithVault = result.results.map(r => ({
            ...r,
            vault: vaultName
          }));

          aggregated.all_results.push(...resultsWithVault);
          aggregated.total_results += result.result_count;
        } else {
          aggregated.results_by_vault[vaultName] = {
            error: result.error,
            result_count: 0,
            results: []
          };
        }
      });

      // Sort all_results by score (descending)
      aggregated.all_results.sort((a, b) => (b.score || 0) - (a.score || 0));

      return aggregated;
    } catch (error) {
      return {
        error: error.message,
        query: query,
        vaults_searched: vaultNames.length,
        results_by_vault: {},
        all_results: [],
        total_results: 0
      };
    }
  }

  /**
   * Get all indexed collections
   *
   * @returns {Promise<Object>} List of collections with document counts
   */
  async getCollections() {
    try {
      const response = await fetch(`${this.baseURL}/collections`, { timeout: 5000 });

      if (!response.ok) {
        throw new Error(`Failed to get collections: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      return {
        collections: [],
        error: error.message
      };
    }
  }

  /**
   * Get status of a specific vault collection
   *
   * @param {string} vaultName - Name of the vault
   * @returns {Promise<Object>} Vault status and document count
   */
  async getVaultStatus(vaultName) {
    try {
      const response = await fetch(
        `${this.baseURL}/status?vault_name=${encodeURIComponent(vaultName)}`,
        { timeout: 5000 }
      );

      if (!response.ok) {
        throw new Error(`Failed to get vault status: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      return {
        vault_name: vaultName,
        status: 'error',
        document_count: 0,
        watcher_active: false,
        error: error.message
      };
    }
  }

  /**
   * Index or re-index a vault
   *
   * @param {string} vaultName - Name of the vault to index
   * @param {number} batchSize - Batch size for indexing (default: 20)
   * @param {boolean} skipExisting - Skip already indexed documents (default: true)
   * @returns {Promise<Object>} Indexing results
   */
  async indexVault(vaultName, batchSize = 20, skipExisting = true) {
    try {
      const response = await fetch(`${this.baseURL}/index`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          vault_name: vaultName,
          batch_size: batchSize,
          skip_existing: skipExisting
        }),
        timeout: 300000 // 5 minutes for indexing
      });

      if (!response.ok) {
        throw new Error(`Indexing failed: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      return {
        status: 'error',
        vault_name: vaultName,
        error: error.message
      };
    }
  }

  /**
   * Start file watcher for a vault
   *
   * @param {string} vaultName - Name of the vault
   * @returns {Promise<Object>} Watcher status
   */
  async startWatcher(vaultName) {
    try {
      const response = await fetch(`${this.baseURL}/watcher/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vault_name: vaultName }),
        timeout: 5000
      });

      if (!response.ok) {
        throw new Error(`Failed to start watcher: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      return {
        status: 'error',
        vault_name: vaultName,
        error: error.message
      };
    }
  }

  /**
   * Stop file watcher for a vault
   *
   * @param {string} vaultName - Name of the vault
   * @returns {Promise<Object>} Watcher status
   */
  async stopWatcher(vaultName) {
    try {
      const response = await fetch(`${this.baseURL}/watcher/stop`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vault_name: vaultName }),
        timeout: 5000
      });

      if (!response.ok) {
        throw new Error(`Failed to stop watcher: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      return {
        status: 'error',
        vault_name: vaultName,
        error: error.message
      };
    }
  }
}

module.exports = RAGClient;
