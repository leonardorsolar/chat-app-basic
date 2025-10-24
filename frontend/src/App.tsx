import Chat from './components/Chat'

function App() {
  console.log("iniciando o App.tsx")
  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4">
      <Chat />
    </div>
  )
}

export default App

//1-Instalar dependências:
//npm install 
//2- Executar:
//npm run dev
// ajuste no src/components/Chat.tsx:
// node : const API_URL = 'http://localhost:3001/api/chat';
// python : const API_URL = 'http://localhost:3002/api/chat';