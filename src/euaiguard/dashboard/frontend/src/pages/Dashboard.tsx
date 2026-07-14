import * as React from "react";

export interface IDashboardProps {}

export default function Dashboard(props: IDashboardProps) {
  const [data, setData] = React.useState<any>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState("");

  React.useEffect(() => {
    fetch("http://localhost:8000/api/article/02")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        return res.json();
      })
      .then((json) => {
        console.log("API Response:", json);
        setData(json);
      })
      .catch((err) => {
        console.error(err);
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return <h2>Loading...</h2>;

  if (error) return <h2>Error: {error}</h2>;

  if (!data) return <h2>No data found.</h2>;


  const installedPackages = data?.auto_detected?.packages?.installed ?? [];
  const usedPackages = data?.auto_detected?.packages?.used ?? [];


  return (
    <div style={{ padding: "20px" }}>
      <h1>EU AI Dashboard</h1>

      <h2>{data.article ?? "Unknown Article"}</h2>

      <table border={1} cellPadding={8}>
        <thead>
          <tr>
            <th>Question</th>
            <th>Answer</th>
          </tr>
        </thead>

        <tbody>
          {Object.entries(data.answers ?? {}).map(([key, value]) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{String(value)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <h1>Used & Detected Packages</h1>
      <div>
        <h2>Installed Packages</h2>
        <ul>
          {Object?.values(installedPackages)?.map((pkg: any, index: number) => (
            <li key={index}>
              {pkg.name} - {pkg.version}
            </li>
          ))}
        </ul>
      </div>

      {/* <h3>Raw API Response</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre> */}
    </div>
  );
}