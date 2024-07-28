import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div>
      <main className="flex flex-col items-center justify-center">
        <h1 className="text-6xl font-bold">Hello World👋</h1>
      </main>
      <footer>
          <Button>Start Here</Button>
      </footer>
    </div>
  )
}
