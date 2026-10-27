import './globals.css';

export const metadata = {
  title: 'MCP Audit',
  description: 'Security audit and risk-scoring marketplace for MCP servers',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
