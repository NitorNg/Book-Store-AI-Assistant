import {useState, useEffect} from 'react'

export default function useChat() {
    const [message, setMessage] = useState("");
    const [messageList, setMessageList] = useState([{}]);
    const [conversationId, setConversationId] = useState(null);
    
    const token = localStorage.getItem("token");
  
    useEffect(() => {
      async function loadChat() {
        const id = await getConversation();
        if (id) {
          await getMessages(id);
        }
      }
      loadChat();
    }, []);
  
    console.log("messageList:", messageList);
    async function getMessages(id) {
      const res = await fetch(`http://localhost:8000/messages/${id}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
  
      if (!res.ok) throw new Error(`Failed to get messages: ${res.status}`);
  
      const data = await res.json();
      console.log("data", data);
      setMessageList(data.messages);
    }

    async function getConversation() {
      const res = await fetch("http://localhost:8000/conversations", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (!res.ok) throw new Error(`Failed to get conversations: ${res.status} `);
  
      const data = await res.json();
      console.log("data", data);
      if (data.conversations.length > 0) {
        const latestConv = data.conversations[data.conversations.length - 1];
        setConversationId(latestConv.id);
        return latestConv.id;
      }
    }
    console.log("conversationid:", conversationId);
  
    async function handleSubmit(e) {
      e.preventDefault();
      const token = localStorage.getItem("token");
  
      if (!message) {
        return;
      }
      setMessageList((prev) => [
        ...prev,
        { role: "user", text: message, created_at: Date.now() },
      ]);
  
      try {
        const res = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            message: message.trim(),
            conversation_id: conversationId,
          }),
        });
  
        if (!res.ok) throw new Error(`Server Error ${res.status}`);
  
        const data = await res.json();
        console.log("data:", data);
        
        setConversationId(data.conversation_id)
        setMessageList((prev) => [...prev, { role: "bot", text: data.reply }]);
      } catch (error) {
        console.error(error);
        setMessageList((prev) => [
          ...prev,
          { role: "bot", text: "Sorry, something went wrong." },
        ]);
      }
      setMessage("");
    }

    return {
      message,
      setMessage,
      handleSubmit,
      messageList
    }
}
