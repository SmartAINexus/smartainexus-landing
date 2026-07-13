export const locales = ["en","bg","cs","da","et","fi","fr","el","nl","hr","ga","pl","lv","lt","hu","mt","de","it","pt","ro","es","sv","sk","sl"] as const;
export type Locale = (typeof locales)[number];

export type Messages = {
  language: string; pilot: string; title: string; subtitle: string; synthetic: string;
  profile: string; matches: string; step: string; of: string; back: string; next: string; finish: string;
  orgTitle: string; orgHelp: string; orgName: string; orgType: string; country: string;
  missionTitle: string; missionHelp: string; mission: string; beneficiaries: string;
  fundingTitle: string; fundingHelp: string; budget: string; cofunding: string;
  reviewTitle: string; reviewHelp: string; complete: string; edit: string;
  matchTitle: string; verified: string; deadline: string; amount: string; score: string;
  why: string; risk: string; interested: string; later: string; irrelevant: string;
};

const en: Messages = {
  language:"Language",pilot:"Romania pilot · synthetic data",title:"Funding readiness workspace",subtitle:"Build your NGO profile and review explainable, supervised grant matches.",synthetic:"Demo only — no real organisation or personal data.",profile:"NGO Profile",matches:"Active Grant Matches",step:"Step",of:"of",back:"Back",next:"Continue",finish:"Complete profile",orgTitle:"Organisation",orgHelp:"Start with the legal basics.",orgName:"Official name",orgType:"Organisation type",country:"Operating country",missionTitle:"Mission & impact",missionHelp:"Tell us whom you serve and why.",mission:"Mission",beneficiaries:"Primary beneficiaries",fundingTitle:"Funding readiness",fundingHelp:"Use approximate, synthetic values for this pilot.",budget:"Annual budget range",cofunding:"Can provide co-funding",reviewTitle:"Review",reviewHelp:"Confirm this synthetic profile before matching.",complete:"Profile ready for supervised review",edit:"Edit profile",matchTitle:"Curated opportunities",verified:"Source verified",deadline:"Deadline",amount:"Amount",score:"Match",why:"Why it fits",risk:"Check before applying",interested:"Interested",later:"Later",irrelevant:"Not relevant"
};

const overrides: Record<Exclude<Locale,"en">, Partial<Messages>> = {
  bg:{language:"Език",profile:"Профил на НПО",matches:"Активни грантове"},
  da:{language:"Sprog",profile:"NGO-profil",matches:"Aktive tilskud"},
  et:{language:"Keel",profile:"MTÜ profiil",matches:"Aktiivsed toetused"},
  fi:{language:"Kieli",profile:"Järjestöprofiili",matches:"Aktiiviset avustukset"},
  el:{language:"Γλώσσα",profile:"Προφίλ ΜΚΟ",matches:"Ενεργές επιχορηγήσεις"},
  nl:{language:"Taal",profile:"NGO-profiel",matches:"Actieve subsidies"},
  hr:{language:"Jezik",profile:"Profil NVO-a",matches:"Aktivni natječaji"},
  ga:{language:"Teanga",profile:"Próifíl ENR",matches:"Deontais ghníomhacha"},
  lv:{language:"Valoda",profile:"NVO profils",matches:"Aktīvie granti"},
  lt:{language:"Kalba",profile:"NVO profilis",matches:"Aktyvios dotacijos"},
  mt:{language:"Lingwa",profile:"Profil tal-NGO",matches:"Għotjiet attivi"},
  pt:{language:"Idioma",profile:"Perfil de ONG",matches:"Apoios ativos"},
  sv:{language:"Språk",profile:"NGO-profil",matches:"Aktiva bidrag"},
  sl:{language:"Jezik",profile:"Profil NVO",matches:"Aktivni razpisi"},
  hu:{language:"Nyelv",pilot:"Romániai pilot · szintetikus adatok",title:"Pályázati felkészültségi munkatér",subtitle:"Készítse el NGO-profilját, és tekintse át a magyarázható, felügyelt pályázati találatokat.",synthetic:"Csak bemutató — ne adjon meg valós szervezeti vagy személyes adatot.",profile:"NGO-profil",matches:"Aktív pályázati találatok",step:"Lépés",of:"/",back:"Vissza",next:"Tovább",finish:"Profil befejezése",orgTitle:"Szervezet",orgHelp:"Kezdje a jogi alapadatokkal.",orgName:"Hivatalos név",orgType:"Szervezeti forma",country:"Működési ország",missionTitle:"Küldetés és hatás",missionHelp:"Mutassa be, kiket és miért támogat.",mission:"Küldetés",beneficiaries:"Elsődleges kedvezményezettek",fundingTitle:"Finanszírozási felkészültség",fundingHelp:"A pilotban közelítő, szintetikus értékeket használjon.",budget:"Éves költségvetési sáv",cofunding:"Képes önrészt biztosítani",reviewTitle:"Áttekintés",reviewHelp:"Erősítse meg a szintetikus profilt az illesztés előtt.",complete:"A profil felügyelt ellenőrzésre kész",edit:"Profil szerkesztése",matchTitle:"Ellenőrzött lehetőségek",verified:"Forrás ellenőrizve",deadline:"Határidő",amount:"Összeg",score:"Illeszkedés",why:"Miért illeszkedik",risk:"Indulás előtt ellenőrizendő",interested:"Érdekel",later:"Később",irrelevant:"Nem releváns"},
  ro:{language:"Limbă",pilot:"Pilot România · date sintetice",title:"Spațiu pentru pregătirea finanțării",subtitle:"Creați profilul ONG și analizați oportunități explicabile, supravegheate.",synthetic:"Doar demonstrație — nu introduceți date reale.",profile:"Profil ONG",matches:"Finanțări active",step:"Pasul",of:"din",back:"Înapoi",next:"Continuă",finish:"Finalizează profilul",orgTitle:"Organizație",orgHelp:"Începeți cu datele juridice de bază.",orgName:"Denumire oficială",orgType:"Tip organizație",country:"Țara de operare",missionTitle:"Misiune și impact",missionHelp:"Descrieți beneficiarii și scopul.",mission:"Misiune",beneficiaries:"Beneficiari principali",fundingTitle:"Pregătire financiară",fundingHelp:"Folosiți valori sintetice aproximative.",budget:"Buget anual",cofunding:"Poate asigura cofinanțare",reviewTitle:"Verificare",reviewHelp:"Confirmați profilul sintetic.",complete:"Profil pregătit pentru verificare",edit:"Editează profilul",matchTitle:"Oportunități verificate",verified:"Sursă verificată",deadline:"Termen",amount:"Sumă",score:"Potrivire",why:"De ce se potrivește",risk:"De verificat",interested:"Interesat",later:"Mai târziu",irrelevant:"Nerelevant"},
  de:{language:"Sprache",title:"Arbeitsbereich Förderbereitschaft",profile:"NGO-Profil",matches:"Aktive Fördertreffer",next:"Weiter",back:"Zurück",finish:"Profil abschließen",orgTitle:"Organisation",missionTitle:"Mission und Wirkung",fundingTitle:"Förderbereitschaft",reviewTitle:"Prüfung"},
  fr:{language:"Langue",title:"Espace de préparation au financement",profile:"Profil ONG",matches:"Financements actifs",next:"Continuer",back:"Retour",finish:"Terminer le profil",orgTitle:"Organisation",missionTitle:"Mission et impact",fundingTitle:"Préparation financière",reviewTitle:"Vérification"},
  es:{language:"Idioma",title:"Espacio de preparación financiera",profile:"Perfil ONG",matches:"Ayudas activas",next:"Continuar",back:"Atrás",finish:"Completar perfil",orgTitle:"Organización",missionTitle:"Misión e impacto",fundingTitle:"Preparación financiera",reviewTitle:"Revisión"},
  it:{language:"Lingua",title:"Area di preparazione ai finanziamenti",profile:"Profilo ONG",matches:"Opportunità attive",next:"Continua",back:"Indietro",finish:"Completa profilo",orgTitle:"Organizzazione",missionTitle:"Missione e impatto",fundingTitle:"Preparazione finanziaria",reviewTitle:"Revisione"},
  pl:{language:"Język",title:"Obszar gotowości finansowej",profile:"Profil NGO",matches:"Aktywne dotacje",next:"Dalej",back:"Wstecz",finish:"Ukończ profil",orgTitle:"Organizacja",missionTitle:"Misja i wpływ",fundingTitle:"Gotowość finansowa",reviewTitle:"Przegląd"},
  sk:{language:"Jazyk",title:"Pracovisko pripravenosti na financovanie",profile:"Profil NGO",matches:"Aktívne granty",next:"Pokračovať",back:"Späť",finish:"Dokončiť profil",orgTitle:"Organizácia",missionTitle:"Poslanie a vplyv",fundingTitle:"Finančná pripravenosť",reviewTitle:"Kontrola"},
  cs:{language:"Jazyk",title:"Prostor připravenosti na financování",profile:"Profil NGO",matches:"Aktivní granty",next:"Pokračovat",back:"Zpět",finish:"Dokončit profil",orgTitle:"Organizace",missionTitle:"Poslání a dopad",fundingTitle:"Finanční připravenost",reviewTitle:"Kontrola"}
};

export const messages = Object.fromEntries(locales.map(locale => [locale, locale === "en" ? en : {...en, ...overrides[locale]}])) as Record<Locale, Messages>;
export type LocaleMetadata = { nativeName:string; intlLocale:string; direction:"ltr"|"rtl"; reviewStatus:"human-reviewed"|"draft" };
export const localeMetadata: Record<Locale,LocaleMetadata> = {
  en:{nativeName:"English",intlLocale:"en-IE",direction:"ltr",reviewStatus:"human-reviewed"},
  bg:{nativeName:"Български",intlLocale:"bg-BG",direction:"ltr",reviewStatus:"draft"},cs:{nativeName:"Čeština",intlLocale:"cs-CZ",direction:"ltr",reviewStatus:"draft"},da:{nativeName:"Dansk",intlLocale:"da-DK",direction:"ltr",reviewStatus:"draft"},et:{nativeName:"Eesti",intlLocale:"et-EE",direction:"ltr",reviewStatus:"draft"},fi:{nativeName:"Suomi",intlLocale:"fi-FI",direction:"ltr",reviewStatus:"draft"},fr:{nativeName:"Français",intlLocale:"fr-FR",direction:"ltr",reviewStatus:"draft"},el:{nativeName:"Ελληνικά",intlLocale:"el-GR",direction:"ltr",reviewStatus:"draft"},nl:{nativeName:"Nederlands",intlLocale:"nl-NL",direction:"ltr",reviewStatus:"draft"},hr:{nativeName:"Hrvatski",intlLocale:"hr-HR",direction:"ltr",reviewStatus:"draft"},ga:{nativeName:"Gaeilge",intlLocale:"ga-IE",direction:"ltr",reviewStatus:"draft"},pl:{nativeName:"Polski",intlLocale:"pl-PL",direction:"ltr",reviewStatus:"draft"},lv:{nativeName:"Latviešu",intlLocale:"lv-LV",direction:"ltr",reviewStatus:"draft"},lt:{nativeName:"Lietuvių",intlLocale:"lt-LT",direction:"ltr",reviewStatus:"draft"},hu:{nativeName:"Magyar",intlLocale:"hu-HU",direction:"ltr",reviewStatus:"draft"},mt:{nativeName:"Malti",intlLocale:"mt-MT",direction:"ltr",reviewStatus:"draft"},de:{nativeName:"Deutsch",intlLocale:"de-DE",direction:"ltr",reviewStatus:"draft"},it:{nativeName:"Italiano",intlLocale:"it-IT",direction:"ltr",reviewStatus:"draft"},pt:{nativeName:"Português",intlLocale:"pt-PT",direction:"ltr",reviewStatus:"draft"},ro:{nativeName:"Română",intlLocale:"ro-RO",direction:"ltr",reviewStatus:"draft"},es:{nativeName:"Español",intlLocale:"es-ES",direction:"ltr",reviewStatus:"draft"},sv:{nativeName:"Svenska",intlLocale:"sv-SE",direction:"ltr",reviewStatus:"draft"},sk:{nativeName:"Slovenčina",intlLocale:"sk-SK",direction:"ltr",reviewStatus:"draft"},sl:{nativeName:"Slovenščina",intlLocale:"sl-SI",direction:"ltr",reviewStatus:"draft"}
};
export const languageNames = Object.fromEntries(locales.map(locale=>[locale,localeMetadata[locale].nativeName])) as Record<Locale,string>;
export function getMessages(locale:string): Messages { return messages[locales.includes(locale as Locale)?locale as Locale:"en"]; }
export type CriticalCopyReview = { sourceLanguage:Locale; sourceText:string; translatedText?:string; status:"source-only"|"draft"|"human-reviewed" };
