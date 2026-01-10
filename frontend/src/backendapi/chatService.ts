export interface ChatResponse {
  type: string;
  content: {
    airesponse: string;
    item_suggested: number[];
  };
}

export interface ProductDetails {
  id: number;
  name: string;
  description: string;
  price: string;
  // Add other fields as expected from backend
}


// Helper to get CSRF token
function getCookie(name: string) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Returns a generator that yields partial updates


export async function* streamChatResponse(storeName: string, prompt: string) {
  const csrftoken = getCookie('csrftoken');
  const response = await fetch(`/${storeName}/api/chat/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken || "",
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch chat response: ${response.statusText}`);
  }

  if (!response.body) {
    throw new Error("Response body is null");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n\n");
    buffer = lines.pop() || ""; // Keep the incomplete line in buffer

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        const dataStr = line.replace("data: ", "").trim();
        if (!dataStr) continue;
        try {
          const data = JSON.parse(dataStr);
          yield data;
        } catch (e) {
          console.error("Error parsing stream data", e);
        }
      }
    }
  }
}



export const fetchProductDetails = async (storeName: string, productId: number): Promise<ProductDetails> => {
  const response = await fetch(`/${storeName}/api/products/${productId}/`);

  if (!response.ok) {
    throw new Error(`Failed to fetch product details for ID ${productId}: ${response.statusText}`);
  }

  return response.json();
};
