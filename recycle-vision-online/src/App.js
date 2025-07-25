import React, { useState } from 'react';
import BarcodeScanner from './BarcodeScanner';
import './App.css'; 

function App() {
  const [scanResult, setScanResult] = useState(null);

  const handleScanResult = (result) => {
    setScanResult(result);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Recycle Vision</h1>
      </header>

      <main>
        {/* The BarcodeScanner component, which contains the file input */}
        <BarcodeScanner onResult={handleScanResult} />

        {/* Display results */}
        {scanResult && (
          <div className="results">
            {scanResult.success ? (
              <>
                <h2>Scan Result</h2>
                <p><strong>Barcode:</strong> {scanResult.barcode}</p>
                <p><strong>Packaging:</strong> {scanResult.packaging}</p>
                <p>
                  <strong>Recyclable:</strong> {scanResult.recyclable ? 'Yes' : 'No'}
                </p>
                <p>
                  <strong>Instructions:</strong> {scanResult.recycling_instructions}
                </p>
              </>
            ) : (
              <p style={{ color: 'red' }}><strong>Error:</strong> {scanResult.error}</p>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;