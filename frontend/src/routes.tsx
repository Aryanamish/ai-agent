import { createBrowserRouter, useLoaderData, Outlet, useOutletContext, useLocation } from "react-router";
import { LandingPage } from "./pages";
import { HomePage } from "./pages/home";
import API from "@/lib/Axios";
import Chat, { ChatWrapper } from "./pages/chat";
import { AppLayout } from "./components/layout";
import { RouteError } from "./error";

// Wrapper to force remount Chat component on route change
const NewChatWrapper = () => {
  const location = useLocation();
  return <Chat key={location.key} />;
};

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

export const ChatLayout = () => {
  const data = useLoaderData().data as OrgDetails;
  return (
    <AppLayout orgName={data.name} orgSlug={data.slug}>
      <Outlet context={{ slug: data.slug }} />
    </AppLayout>
  );
};
const ContextForwardingOutlet = () => {
  const context = useOutletContext();
  return <Outlet context={context} />;
};

const loginCheck = async () => {
  // lazy implementation of login check because i dont have time to set up proper auth flow.

  try {
    await API.get("/api/organizations/")
  } catch (e) {
    // @ts-expect-error
    if (e?.response?.status < 500 && e?.response?.status >= 400) {
      window.location.href = "/admin/login/";
    }
    throw new Response("Something went wront", { status: 500 });
  }
}

export const router = createBrowserRouter([
  {
    path: "/",
    loader: async()=>{
      await loginCheck()
      window.location.href = "/store"
    },
    element: <LandingPage></LandingPage>,
    errorElement: <RouteError />

  },
  {
    path: "/store",
    loader: async () => {
      loginCheck()
      try {
        const data = await API.get("/api/organizations/");
        return data
      } catch (e) {
        throw new Response("Organizations not found", { status: 500 });
      }

    },
    element: <HomePage></HomePage>,
    errorElement: <RouteError />
  },
  {
    path: "/:slug",
    errorElement: <RouteError />,
    loader: async ({ params }) => {
      loginCheck()
      try {
        const data = await API.get(`/api/organizations/${params.slug}`);
        return data;
      } catch (e) {
        throw new Response("Organization not found", { status: 404 });
      }

    },
    element: <ChatLayout />,
    children: [
      {
        path: "chat",
        element: <ContextForwardingOutlet />,
        children: [
          {
            index: true,
            element: <NewChatWrapper />
          }, {
            path: ":chatRoomId",
            loader: async ({ params }) => {
              try {
                const data = await API.get(`/${params.slug}/api/chat/history/${params.chatRoomId}/`)
                return data
              } catch (e) {
                throw new Response("Organization not found", { status: 404 });
              }
            },
            element: <ChatWrapper />
          }
        ]
      },
    ]
  },

])




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