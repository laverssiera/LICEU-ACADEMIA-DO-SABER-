import type { ReactNode } from "react";

export const metadata = {
  title: "LICEU Academia",
  description: "Sistema Operacional Educacional Cognitivo",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
