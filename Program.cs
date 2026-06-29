using System;
using System.Diagnostics;
using System.Net;
using System.Threading;
using System.Threading.Tasks;


namespace PROMPT
{
    internal class Program
    {
        static async Task Main(string[] args)
        {
            Banner();
            while (true)
            {
                Console.ForegroundColor = ConsoleColor.Red;

                Console.Write("[USR]>> : ");
                string CMD = Console.ReadLine()?.ToLower()?.Trim();
                if (string.IsNullOrWhiteSpace(CMD)) continue;

                else if (CMD.StartsWith("op>") || CMD.StartsWith("open"))
                {
                    Open(CMD);
                }
                else if (CMD.StartsWith("b>"))
                {
                    Browse(CMD);
                }
                else if (CMD == "help" || CMD == "--help")
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine("""
                        COMMAND HELP-LINE!
                        1. 'help' -> Displays this Command help-line.
                        2. 'op> <URL/APP>' -> Opens the given website, or app.
                        3. 'b> <QUERY/URL>' -> Searches your query on the web.
                        4. 'Environment.<deviceinfo>' -> for device queries.
                        5. 'exit' or 'ter!' -> Exits the assistant.
                        """);
                    Console.ResetColor();
                }
                else if (CMD == "exit" || CMD == "ter!")
                {
                    Typewrite("PROGRAM TERMIANTED !");
                    break;
                }
                else
                {
                    Typewrite("Unknown command. Type 'help' for usage.");
                }
            }
        }
        static void Browse(string Query)
        {
            string Qy = Query.ToLower().Replace("Browse", "").Replace("b>", "");
            string k;
            Typewrite($"Browsing about {Qy}");
            k = @"https://www.duckduckgo.com/?q=" + WebUtility.UrlEncode(Qy);
                try
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = k,
                        UseShellExecute = true
                    });
                }
                catch (Exception ex)
                {
                    Typewrite($"ERROR! {ex.Message}");
                }
        }
        static void Open(string x)
        {
            string BASE = x.ToLower().Replace("open", "").Replace("op>", "").Trim();

            try
            {
                if (File.Exists(BASE) || Directory.Exists(BASE))
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = BASE,
                        UseShellExecute = true
                    });
                    Typewrite($"Opening local path: {BASE}");
                }
                if (BASE == "notepad" || BASE == "calc" || BASE == "cmd" || BASE == "edge" || BASE == "spotify")
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = BASE,
                        UseShellExecute = true
                    });
                    Typewrite($"Launching app: {BASE}");
                }
                else
                {
                    if (!BASE.StartsWith("http"))
                    {
                        if (BASE.StartsWith("www."))
                            BASE = "https://" + BASE;
                        else
                            BASE = "https://www." + BASE;
                    }

                    Process.Start(new ProcessStartInfo
                    {
                        FileName = BASE,
                        UseShellExecute = true
                    });
                    Typewrite($"Opening website: {BASE}");
                }
            }
            catch (Exception ex)
            {
                Typewrite($"ERROR! {ex.Message}");
            }
        }
        static async Task GlowAsync(string text, int x, int y)
        {
            ConsoleColor[] glow =
            {
              ConsoleColor.DarkCyan,
              ConsoleColor.Cyan,
              ConsoleColor.White,
              ConsoleColor.Cyan
            };

            while (true)
            {
                foreach (var color in glow)
                {
                    Console.SetCursorPosition(x, y);
                    Console.ForegroundColor = color;
                    Console.Write(text);
                    await Task.Delay(120);
                }
            }
        }
        static void Banner()
        {
            string BANNER = @"
  _____     ______    _____    _______    _____    _______
 |_____]   |_____/   |     |   |  |  |   |_____]      |   
 |       . |    \_ . |_____| . |  |  | . |       .    |   
 ====================== RED-DEVIL ========================

";
            Console.ForegroundColor = ConsoleColor.Red;
            Typewrite(BANNER, 5);
            Console.ResetColor();
        }

        static void Typewrite(string text, int delay = 30)
        {
            foreach (char c in text)
            {
                Console.Write(c);
                Thread.Sleep(delay);
            }
            Console.WriteLine();
        }
    }
}
