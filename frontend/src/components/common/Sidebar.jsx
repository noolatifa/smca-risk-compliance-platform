export default function Sidebar({ page, setPage }) {
  function classeNavigation(nomPage) {
    return page === nomPage
      ? "nav-link active"
      : "nav-link";
  }

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-logo">S</div>

        <div>
          <h1>SMCA</h1>
          <span>Risk Compliance</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <button
          type="button"
          className={classeNavigation("dashboard")}
          onClick={() => setPage("dashboard")}
        >
          <span>▦</span>
          Dashboard
        </button>

        <button
          type="button"
          className={classeNavigation("referentiel")}
          onClick={() => setPage("referentiel")}
        >
          <span>◈</span>
          Référentiel
        </button>

        <button
          type="button"
          className={classeNavigation("bia")}
          onClick={() => setPage("bia")}
        >
          <span>◉</span>
          BIA
        </button>

        <button
          type="button"
          className={classeNavigation("risques")}
          onClick={() => setPage("risques")}
        >
          <span>⚠</span>
          Risques
        </button>

        <button
          type="button"
          className={classeNavigation("traitements")}
          onClick={() => setPage("traitements")}
        >
          <span>✓</span>
          Traitements
        </button>

        <button
          type="button"
          className={classeNavigation("cartographie")}
          onClick={() => setPage("cartographie")}
        >
          <span>▦</span>
          Cartographie
        </button>

        <button
          type="button"
          className={classeNavigation("exports")}
          onClick={() => setPage("exports")}
        >
          <span>⇩</span>
          Exports
        </button>
      </nav>

      <div className="api-status">
        <span></span>
        API connectée
      </div>
    </aside>
  );
}