import React, { useState } from "react";
import FileUpload from "./FileUpload";
import ResultCard from "./ResultCard";

const Dashboard: React.FC = () => {
  const [result, setResult] = useState<any>(null);

  return (
    <div className="max-w-2xl mx-auto mt-10">
      <h1 className="text-3xl font-bold text-center mb-6">
        🧩 Attestation Policy Enforcer
      </h1>
      <FileUpload onUploadSuccess={setResult} />
      <ResultCard data={result} />
    </div>
  );
};

export default Dashboard;
