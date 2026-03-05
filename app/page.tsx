<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-7xl mx-auto">
  {[
    { title: "I'm a Manufacturer", desc: "Gyártóként csatlakozz a jövőhöz..." },
    { title: "I'm a Business Buyer", desc: "Üzleti vevőként találj partnereket..." },
    { title: "I'm an Individual Buyer", desc: "Magánvevőként vásárolj okosan..." },
    { title: "I'm a Builder", desc: "Építs és tesztelj velünk..." },
  ].map((item) => (
    <div
      key={item.title}
      className="group relative bg-gray-900/50 backdrop-blur-xl border border-cyan-500/30 rounded-2xl p-8 hover:border-cyan-400 hover:scale-105 transition-all duration-500 cursor-pointer shadow-2xl"
      onClick={() => {
        // Semmi nem történik – marad a főoldalon
        // Később ide jöhet pl. modal: "Hamamosan elérhető!"
      }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity" />
      <h3 className="text-3xl font-bold text-center mb-4 text-cyan-300 group-hover:text-cyan-100">
        {item.title}
      </h3>
      <p className="text-gray-400 text-center">
        {item.desc}
      </p>
    </div>
  ))}
</div>
