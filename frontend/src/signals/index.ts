import { effect, signal } from "@preact/signals-react";


const ThemeSignal = signal<'light' | 'dark'>(localStorage.getItem("theme") === "dark" ? 'dark' : 'light');

effect(()=>{
  const html = document.getElementsByTagName("html")[0]
  html.classList.remove('light')
  html.classList.remove('dark')
  html.classList.add(ThemeSignal.value)
  localStorage.setItem("theme", ThemeSignal.value);

})

const StoreNameSignal = signal<string>('ABC');
const ChatHistorySignal = signal<{
  name: string,
  url: string
}[]>([]);

const ChatMessagesSignal = signal<string[]>([])

export { ThemeSignal,StoreNameSignal, ChatHistorySignal ,ChatMessagesSignal};