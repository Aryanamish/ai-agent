import { useRouteError, isRouteErrorResponse } from "react-router";

export const RouteError = () => {
  const error = useRouteError();

  if (isRouteErrorResponse(error)) {
    if (error.status === 404) {
      return (
        <div className="w-full h-screen flex justify-center items-center gap-2">
          <h1>404</h1>
          <p>Page not found</p>
        </div>
      );
    }

    if (error.status === 500) {
      return (
        <div className="w-full h-screen flex justify-center items-center gap-2">
          <h1>500</h1>
          <p>Internal server error</p>
        </div>
      );
    }

    return (
      <div className="w-full h-screen flex justify-center items-center gap-2">
        <h1>{error.status}</h1>
        <p>{error.statusText}</p>
      </div>
    );
  }

  return (
    <div className="w-full h-screen flex justify-center items-center gap-2">
      <h1>Unexpected Error</h1>
      <p>Something went wrong.</p>
    </div>
  );
};
