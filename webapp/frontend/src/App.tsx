import React, { useState, useEffect, useRef } from 'react';
import { Play, Copy, Download, Globe, Zap, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import './App.css';

interface TestSession {
  session_id: string;
  status: string;
  url: string;
  test_name: string;
  completed: boolean;
  output: string[];
  results?: any;
}

interface StructuredData {
  website_info: any;
  content_statistics: any;
  test_results: any[];
  ai_analysis: string;
  final_assessment: any;
}

function App() {
  const [url, setUrl] = useState('');
  const [testName, setTestName] = useState('Website Test');
  const [isRunning, setIsRunning] = useState(false);
  const [currentSession, setCurrentSession] = useState<TestSession | null>(null);
  const [terminalOutput, setTerminalOutput] = useState<string[]>([]);
  const [structuredData, setStructuredData] = useState<StructuredData | null>(null);
  const [wsConnection, setWsConnection] = useState<WebSocket | null>(null);
  const terminalRef = useRef<HTMLDivElement>(null);

  // Auto-scroll terminal to bottom
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [terminalOutput]);

  const startTest = async () => {
    if (!url.trim()) {
      alert('Please enter a website URL');
      return;
    }

    setIsRunning(true);
    setTerminalOutput([]);
    setStructuredData(null);

    try {
      // Start the test
      const response = await fetch('/run-test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url.trim(),
          test_name: testName.trim(),
        }),
      });

      const data = await response.json();
      
      if (data.session_id) {
        setCurrentSession({
          session_id: data.session_id,
          status: 'starting',
          url: url.trim(),
          test_name: testName.trim(),
          completed: false,
          output: [],
        });

        // Connect to WebSocket for real-time updates
        connectWebSocket(data.session_id);
        
        // Start polling for status updates
        pollTestStatus(data.session_id);
      }
    } catch (error) {
      console.error('Error starting test:', error);
      setTerminalOutput(prev => [...prev, `❌ Error starting test: ${error}`]);
      setIsRunning(false);
    }
  };

  const connectWebSocket = (sessionId: string) => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);
    
    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'output') {
          setTerminalOutput(prev => [...prev, data.message]);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    setWsConnection(ws);
  };

  const pollTestStatus = async (sessionId: string) => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch(`/test-status/${sessionId}`);
        const data = await response.json();
        
        setCurrentSession(prev => prev ? { ...prev, ...data } : null);

        if (data.completed) {
          clearInterval(pollInterval);
          setIsRunning(false);
          
          // Get structured report
          try {
            const reportResponse = await fetch(`/parsed-report/${sessionId}`);
            const reportData = await reportResponse.json();
            setStructuredData(reportData.structured_data);
          } catch (error) {
            console.error('Error fetching report:', error);
          }

          // Close WebSocket
          if (wsConnection) {
            wsConnection.close();
            setWsConnection(null);
          }
        }
      } catch (error) {
        console.error('Error polling status:', error);
        clearInterval(pollInterval);
        setIsRunning(false);
      }
    }, 1000);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // You could add a toast notification here
  };

  const exportToCSV = () => {
    if (!structuredData) return;

    const csvData = [
      ['Test Results'],
      ['URL', structuredData.website_info?.url || ''],
      ['Title', structuredData.website_info?.title || ''],
      ['Analysis Time', structuredData.website_info?.analysis_time || ''],
      [],
      ['Test Results'],
      ['Test', 'Status', 'Details', 'Time'],
      ...structuredData.test_results?.map((result: any) => [
        result.test,
        result.status,
        result.details,
        result.time
      ]) || [],
      [],
      ['Content Statistics'],
      ['Metric', 'Count', 'Details'],
      ...Object.entries(structuredData.content_statistics || {}).map(([key, value]: [string, any]) => [
        key,
        value.count,
        value.details
      ]),
      [],
      ['AI Analysis'],
      [structuredData.ai_analysis || ''],
      [],
      ['Final Assessment'],
      ['Overall Assessment', structuredData.final_assessment?.overall || ''],
      ['Success Rate', structuredData.final_assessment?.success_rate || ''],
      ['Recommendation', structuredData.final_assessment?.recommendation || '']
    ];

    const csvContent = csvData.map(row => row.map(cell => `"${cell}"`).join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `website-test-${Date.now()}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      case 'running':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-500" />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Globe className="w-8 h-8 text-blue-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">Intelligent Website Tester</h1>
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            AI-powered website testing with Orgo virtual desktops. Test any website's functionality, 
            analyze content, and get detailed insights in real-time.
          </p>
        </div>

        {/* Input Form */}
        <div className="card max-w-4xl mx-auto mb-8">
          <div className="card-header">
            <h2 className="card-title">Start a New Test</h2>
            <p className="card-subtitle">Enter a website URL to begin intelligent testing</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Website URL
              </label>
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com"
                className="input-field"
                disabled={isRunning}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Test Name
              </label>
              <input
                type="text"
                value={testName}
                onChange={(e) => setTestName(e.target.value)}
                placeholder="My Test"
                className="input-field"
                disabled={isRunning}
              />
            </div>
          </div>
          
          <div className="mt-6">
            <button
              onClick={startTest}
              disabled={isRunning || !url.trim()}
              className="btn-primary flex items-center justify-center w-full md:w-auto"
            >
              {isRunning ? (
                <>
                  <Zap className="w-4 h-4 mr-2 animate-pulse" />
                  Running Test...
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 mr-2" />
                  Run Test
                </>
              )}
            </button>
          </div>
        </div>

        {/* Terminal Output */}
        {terminalOutput.length > 0 && (
          <div className="card max-w-4xl mx-auto mb-8">
            <div className="card-header">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <h2 className="card-title">Live Terminal Output</h2>
                  {currentSession && (
                    <div className="flex items-center ml-4">
                      {getStatusIcon(currentSession.status)}
                      <span className="ml-2 text-sm font-medium capitalize">
                        {currentSession.status}
                      </span>
                    </div>
                  )}
                </div>
                <button
                  onClick={() => copyToClipboard(terminalOutput.join('\n'))}
                  className="btn-secondary flex items-center"
                >
                  <Copy className="w-4 h-4 mr-2" />
                  Copy
                </button>
              </div>
            </div>
            
            <div 
              ref={terminalRef}
              className="terminal"
            >
              {terminalOutput.map((line, index) => (
                <div key={index} className="terminal-line">
                  {line}
                </div>
              ))}
              {isRunning && (
                <div className="terminal-line loading-dots">
                  Running test
                </div>
              )}
            </div>
          </div>
        )}

        {/* Structured Results */}
        {structuredData && (
          <div className="card max-w-4xl mx-auto mb-8">
            <div className="card-header">
              <div className="flex items-center justify-between">
                <h2 className="card-title">Test Results</h2>
                <button
                  onClick={exportToCSV}
                  className="btn-success flex items-center"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Export CSV
                </button>
              </div>
            </div>

            {/* Website Information */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Website Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gray-50 p-3 rounded-lg">
                  <div className="text-sm text-gray-600">URL</div>
                  <div className="font-medium">{structuredData.website_info?.url || 'N/A'}</div>
                </div>
                <div className="bg-gray-50 p-3 rounded-lg">
                  <div className="text-sm text-gray-600">Title</div>
                  <div className="font-medium">{structuredData.website_info?.title || 'N/A'}</div>
                </div>
                <div className="bg-gray-50 p-3 rounded-lg">
                  <div className="text-sm text-gray-600">Analysis Time</div>
                  <div className="font-medium">{structuredData.website_info?.analysis_time || 'N/A'}</div>
                </div>
              </div>
            </div>

            {/* Test Results Table */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Test Results</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Test
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Details
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Time
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {structuredData.test_results?.map((result: any, index: number) => (
                      <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {result.test}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            result.status.includes('PASS') 
                              ? 'bg-green-100 text-green-800' 
                              : result.status.includes('FAIL')
                              ? 'bg-red-100 text-red-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {result.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500">
                          {result.details}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {result.time}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Content Statistics */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Content Statistics</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(structuredData.content_statistics || {}).map(([key, value]: [string, any]) => (
                  <div key={key} className="bg-blue-50 p-4 rounded-lg text-center">
                    <div className="text-2xl font-bold text-blue-600">{value.count}</div>
                    <div className="text-sm text-blue-800">{key}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* AI Analysis */}
            {structuredData.ai_analysis && (
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">AI Analysis</h3>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <pre className="whitespace-pre-wrap text-sm text-gray-700">
                    {structuredData.ai_analysis}
                  </pre>
                </div>
              </div>
            )}

            {/* Final Assessment */}
            {structuredData.final_assessment && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Final Assessment</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-green-50 p-4 rounded-lg">
                    <div className="text-sm text-green-600">Overall Assessment</div>
                    <div className="text-lg font-semibold text-green-800">
                      {structuredData.final_assessment.overall || 'N/A'}
                    </div>
                  </div>
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <div className="text-sm text-blue-600">Success Rate</div>
                    <div className="text-lg font-semibold text-blue-800">
                      {structuredData.final_assessment.success_rate || 'N/A'}
                    </div>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <div className="text-sm text-purple-600">Recommendation</div>
                    <div className="text-lg font-semibold text-purple-800">
                      {structuredData.final_assessment.recommendation || 'N/A'}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App; 