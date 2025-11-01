import React, { useState } from "react";

interface Props {
  onUploadSuccess: (data: any) => void;
}

const FileUpload: React.FC<Props> = ({ onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first!");
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/scan", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      onUploadSuccess(data);
    } catch (err) {
      alert("Upload failed. Check backend.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 border rounded-2xl shadow-md flex flex-col gap-4 items-center">
      <h2 className="text-xl font-semibold">Upload Dependency File</h2>
        <input
  type="file"
  onChange={handleFileChange}
  accept="*/*"
/>
      <button
        onClick={handleUpload}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded-xl hover:bg-blue-700"
      >
        {loading ? "Scanning..." : "Scan File"}
      </button>
    </div>
  );
};

export default FileUpload;
