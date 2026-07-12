const launchPrinciples = [
  "Csak ellenőrzött pályázati források",
  "Magyarázható jogosultsági és illeszkedési elemzés",
  "Kötelező emberi és ügyféloldali jóváhagyások",
  "Szervezetenként elkülönített, auditálható adatok",
];

export default function Home() {
  return (
    <main>
      <nav className="nav" aria-label="Fő navigáció">
        <a className="brand" href="#top" aria-label="GrantBridge Europe kezdőlap">
          <span className="brandMark">GB</span>
          <span>GrantBridge Europe</span>
        </a>
        <span className="pilotBadge">Romániai pilot előkészítés</span>
      </nav>

      <section className="hero" id="top">
        <div className="eyebrow">Európai nonprofit támogatási platform</div>
        <h1>A megfelelő támogatástól a kész pályázatig.</h1>
        <p className="lead">
          A GrantBridge Europe segít a nonprofit szervezeteknek rendszerezni az adataikat,
          ellenőrzött támogatási lehetőségeket találni és biztonságos, felügyelt folyamatban
          előkészíteni pályázataikat.
        </p>
        <div className="actions">
          <a className="primary" href="#pilot">Pilot áttekintése</a>
          <a className="secondary" href="#principles">Működési alapelvek</a>
        </div>
      </section>

      <section className="panel" id="pilot">
        <div>
          <div className="sectionLabel">Első kiadás</div>
          <h2>Kontrollált, meghívásos romániai pilot</h2>
        </div>
        <p>
          Ez a tiszta alkalmazásalap még nem fogad valódi ügyféladatot és nem végez hivatalos
          benyújtást. A következő fejlesztési lépések a szervezeti profil, a dokumentumtár,
          a pályázati nyilvántartás és Elena digitális ügyintéző biztonságos felépítése.
        </p>
      </section>

      <section className="principles" id="principles" aria-labelledby="principles-title">
        <div className="sectionLabel">Nem alku tárgya</div>
        <h2 id="principles-title">Bizalomra tervezett működés</h2>
        <div className="grid">
          {launchPrinciples.map((principle, index) => (
            <article className="card" key={principle}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <h3>{principle}</h3>
            </article>
          ))}
        </div>
      </section>

      <footer>
        <strong>GrantBridge Europe</strong>
        <span>Szökőcs Green SRL · Szilágy megye, Románia</span>
      </footer>
    </main>
  );
}
