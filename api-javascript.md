# Using the Flight Ticket OCR API with Axios

Here's how you can use the Flight Ticket OCR API with Axios in a JavaScript application:

```javascript
// Example using Axios to call the Flight Ticket OCR API
import axios from 'axios';

/**
 * Extract information from a flight ticket using the OCR API
 * @param {File} file - The flight ticket file (image or PDF)
 * @param {string} model - The AI model to use (optional)
 * @returns {Promise} - Promise resolving to the extracted ticket information
 */
async function extractTicketInfo(file, model = 'deepseek/DeepSeek-V3-0324') {
  // Create form data
  const formData = new FormData();
  formData.append('file', file);
  formData.append('model', model);
  
  try {
    // Make the API request
    const response = await axios.post('http://localhost:8808/api/extract', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    // Return the extracted information
    return response.data;
  } catch (error) {
    // Handle errors
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Error response:', error.response.data);
      throw new Error(error.response.data.error || 'Failed to extract ticket information');
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received:', error.request);
      throw new Error('No response from server');
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Request error:', error.message);
      throw new Error('Error making request');
    }
  }
}

// Example usage in a React component
function TicketUploader() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const ticketInfo = await extractTicketInfo(file);
      setResult(ticketInfo);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      <input type="file" accept=".jpg,.jpeg,.png,.pdf" onChange={handleFileUpload} />
      {loading && <p>Processing ticket...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && (
        <div>
          <h2>Ticket Information</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
```

## Complete Example with Vue.js

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flight Ticket OCR</title>
  <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
    }
    .container {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .form-group {
      margin-bottom: 15px;
    }
    button {
      padding: 8px 16px;
      background-color: #4CAF50;
      color: white;
      border: none;
      cursor: pointer;
      border-radius: 4px;
    }
    button:disabled {
      background-color: #cccccc;
      cursor: not-allowed;
    }
    .result {
      background-color: #f5f5f5;
      padding: 15px;
      border-radius: 4px;
      white-space: pre-wrap;
    }
    .error {
      color: red;
    }
  </style>
</head>
<body>
  <div id="app" class="container">
    <h1>Flight Ticket OCR</h1>
    
    <div class="form-group">
      <label for="file">Upload Flight Ticket (Image or PDF):</label>
      <input type="file" id="file" @change="handleFileChange" accept=".jpg,.jpeg,.png,.pdf">
    </div>
    
    <div class="form-group">
      <label for="model">Select AI Model:</label>
      <select id="model" v-model="selectedModel">
        <option value="deepseek/DeepSeek-V3-0324">DeepSeek Chat</option>
        <option value="anthropic/claude-3-haiku:beta">Claude 3 Haiku</option>
        <option value="anthropic/claude-3-sonnet:beta">Claude 3 Sonnet</option>
        <option value="meta-llama/llama-3-8b-instruct:free">Llama 3 8B</option>
      </select>
    </div>
    
    <button @click="processTicket" :disabled="!selectedFile || loading">
      {{ loading ? 'Processing...' : 'Extract Ticket Information' }}
    </button>
    
    <div v-if="error" class="error">
      <strong>Error:</strong> {{ error }}
    </div>
    
    <div v-if="result" class="result">
      <h2>Extracted Information:</h2>
      <pre>{{ JSON.stringify(result, null, 2) }}</pre>
    </div>
  </div>
  
  <script>
    const { createApp, ref } = Vue;
    
    createApp({
      setup() {
        const selectedFile = ref(null);
        const selectedModel = ref('deepseek/DeepSeek-V3-0324');
        const result = ref(null);
        const loading = ref(false);
        const error = ref(null);
        
        function handleFileChange(event) {
          selectedFile.value = event.target.files[0];
          // Clear previous results
          result.value = null;
          error.value = null;
        }
        
        async function processTicket() {
          if (!selectedFile.value) return;
          
          loading.value = true;
          error.value = null;
          
          const formData = new FormData();
          formData.append('file', selectedFile.value);
          formData.append('model', selectedModel.value);
          
          try {
            const response = await axios.post('http://localhost:8808/api/extract', formData, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            });
            
            result.value = response.data;
          } catch (err) {
            if (err.response) {
              error.value = err.response.data.error || 'Failed to extract ticket information';
            } else if (err.request) {
              error.value = 'No response from server. Make sure the API is running.';
            } else {
              error.value = 'Error making request: ' + err.message;
            }
          } finally {
            loading.value = false;
          }
        }
        
        return {
          selectedFile,
          selectedModel,
          result,
          loading,
          error,
          handleFileChange,
          processTicket
        };
      }
    }).mount('#app');
  </script>
</body>
</html>
```

You can save this HTML file and open it in a browser to test the API. Make sure your API server is running on port 8808 before testing.