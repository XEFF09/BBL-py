import FirstPageProvider from "@/provider/FirstPageProvider";
import "./globals.css";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`h-full antialiased`}>
      <body className="min-h-full flex flex-col">
        <FirstPageProvider>{children}</FirstPageProvider>
      </body>
    </html>
  );
}
