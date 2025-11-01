import React from "react";

interface Props {
  data: any;
}

const ResultCard: React.FC<Props> = ({ data }) => {
  if (!data) return null;

  return (
    <div className="mt-6 p-6 border rounded-2xl shadow-lg">
      <h3 className="text-lg font-bold">Scan Results</h3>
      <p><strong>Detected Licenses:</strong> {data.detected.join(", ")}</p>
      <p><strong>Violations:</strong> {data.violations.join(", ") || "None"}</p>
      <p><strong>Compliance Score:</strong> {data.compliance_score}%</p>
    </div>
  );
};

export default ResultCard;
