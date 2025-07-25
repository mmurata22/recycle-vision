import React, { useState } from 'react';

export default function BarcodeScanner({ onResult }) {
  const [isScanning, setIsScanning] = useState(false);
  const [imagePreviewUrl, setImagePreviewUrl] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log('File selected:', file.name);
      setImagePreviewUrl(URL.createObjectURL(file));
      decodeImage(file);
    }
  };

  const decodeImage = async (imageFile) => {
    setIsScanning(true);
    
    // Create a FormData object to send the file
    const formData = new FormData();
    formData.append('image', imageFile);

    try {
      console.log('Sending file to backend...');
      // The API endpoint you created in server.py
      const response = await fetch('http://127.0.0.1:5000/scan_barcode', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      console.log('Received response from backend:', data);

      // Pass the entire data object to the parent component
      onResult(data);
      
      // Clean up the object URL after processing
      if (imagePreviewUrl) {
        URL.revokeObjectURL(imagePreviewUrl);
      }
      
    } catch (err) {
      console.error('API call failed:', err);
      onResult({ success: false, error: 'Failed to connect to the server or process the image.' });
    } finally {
      setIsScanning(false);
    }
  };

  return (
    <div>
      <h3>Upload Barcode Image</h3>
      <input 
        type="file" 
        accept="image/*" 
        onChange={handleFileChange} 
        disabled={isScanning}
      />
      
      {isScanning && <p>Scanning...</p>}

      {imagePreviewUrl && (
        <div>
          <h4>Uploaded Image Preview:</h4>
          <img 
            src={imagePreviewUrl} 
            alt="Uploaded for barcode scanning" 
            style={{ maxWidth: '100%', maxHeight: '400px' }} 
          />
        </div>
      )}
    </div>
  );
}