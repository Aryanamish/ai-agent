import axios from "axios";

function getCookie(name: string) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const axiosAgent = axios.create({
  baseURL: "/",
  timeout: 10000,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": getCookie("csrftoken"),
  },
});

class API {
  get(...args: Parameters<typeof axiosAgent.get>) {
    return axiosAgent.get(...args);
  }
  post(...args: Parameters<typeof axiosAgent.post>) {
    return axiosAgent.post(...args);
  }
  async stream(
    url: string,
		data:any,
    options: any,
    onMessage: (msg: any) => void,
    onEnd: (msg: any) => void,
    onError: (msg: any) => void
  ) {
    if (!options) {
      options = {};
    }
    if (!options.headers) {
      options.headers = {
        "X-CSRFToken": getCookie("csrftoken"),
      };
    }
    if (!options.headers["X-CSRFToken"]) {
      options.headers["X-CSRFToken"] = getCookie("csrftoken");
    }
		if(data){
			options.method = "POST"
			options.body = JSON.stringify(data)
		}
    const response = await fetch(url, options);
    if (!response.body) {
      throw new Error("Streaming Not supported");
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let uncompleteMessage = "";
		let dump =""
		try{

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      uncompleteMessage += chunk.trim().replace(/^data: /, "");
			dump += chunk;
			onMessage(uncompleteMessage);
    }
		onEnd(dump)
		}catch(err){
			console.error(dump, err);
			onError(dump)
		}

  }
}

export default new API();
