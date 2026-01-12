
import { useEffect } from "react";
import { useNavigate } from "react-router";
import API from "@/lib/Axios";

export function LandingPage() {
  const navigate = useNavigate();

  useEffect(() => {
    const controller = new AbortController();
    API.get("/api/organizations/", { signal: controller.signal })
      .then(() => {
        navigate("/store");
      })
      .catch((err) => {
        if(err.code === "ERR_CANCELED") return;
        window.location.href = "/admin/login/";
      });
    return () => {
      controller.abort();
    }
  }, [navigate]);

  return <></>;
}
