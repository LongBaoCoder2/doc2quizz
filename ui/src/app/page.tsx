import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center mt-[10rem] gap-20">
      <main>
        <h1 className="text-6xl font-bold">Hello World👋</h1>
      </main>
      <footer>
          <Link href="/quizz">
            <Button>Start here</Button>
          </Link>
      </footer>
    </div>
  )
}
