export default function MetricCard({ label, value, color }) {
  return (
    <article className="metric-card">
      <div className={`metric-indicator ${color}`}></div>

      <div>
        <p className="metric-label">{label}</p>
        <p className="metric-value">{value ?? 0}</p>
      </div>
    </article>
  );
}