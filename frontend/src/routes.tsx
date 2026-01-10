import { Routes, Route } from "react-router";
import { LandingPage } from "./pages";
import { HomePage } from "./pages/home";
import { useEffect, useState } from "react";
import API from "@/lib/Axios";
import NewChat from "./pages/new_chat";
import Chat, { ChatWrapper } from "./pages/chat";
import { AppLayout } from "./components/layout";


export interface OrgDetails {
  "id": number,
  "name": string,
  "slug": string,
  "address": string,
  "created_at": string,
  "domain": string,
  "required_attributes": string,
  "system_prompt": string
}

export function ShopwiseRoutes() {
  const [data, setData] = useState<OrgDetails[] | null>(null)
  useEffect(() => {
    const controller = new AbortController();
    API.get("api/organizations/", { signal: controller.signal }).then(({ data }: { data: OrgDetails[] }) => {
      console.log(data);
      setData(data)
    })
    return () => {
      controller.abort();
    }
  }, [])

  return <Routes>
    <Route path="/" element={<LandingPage></LandingPage>} />
    <Route path="/store" element={<HomePage orgs={data}></HomePage>} />
    {data?.map((org) => {
      return <>
        <Route path={`/${org.slug}/chat`} element={<AppLayout orgName={org.name} key={org.id}><Chat slug={org.slug} /></AppLayout>} />
        <Route path={`/${org.slug}/chat/:chatRoomId`} element={<AppLayout orgName={org.name} key={org.id}><ChatWrapper slug={org.slug} /></AppLayout>} />
      </>
    })}
  </Routes>
}