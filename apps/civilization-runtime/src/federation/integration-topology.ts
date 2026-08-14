export const INTEGRATED_MONOLITHS = [
  "P&D",
  "JOHN_BRASILEIRO",
  "CEFEIDA_3C273",
  "BIMARQENG",
  "OPERA",
  "ANCHORS",
  "GAME_MKT",
  "ECONOTECH",
  "FORNECEDORES",
  "CEA",
  "ARCHIMEDES",
  "HUB_BACKOFFICE",
  "JURIDICOTECH"
] as const

export function federationIdentity() {
  return {
    name: "ACADEMIA_DO_SABER",
    role: "civilization-education-runtime"
  }
}
