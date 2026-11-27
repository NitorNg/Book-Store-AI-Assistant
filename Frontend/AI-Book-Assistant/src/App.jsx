import React from "react";
import useChat from '../hooks/useChat.js'
import "./index.css";
import { IoIosSend } from "react-icons/io";

function App() {

  const {message, setMessage, handleSubmit, messageList} = useChat()
  console.log("messageList:", messageList);
  return (
    <div className="flex justify-center items-center h-screen">
      <div className="flex flex-col justify-between border w-140 h-190 rounded-xl">
        {/*     FIRST    */}
        <div className="w-full h-20 border border-blue-500">
          BookStore Assistant
        </div>

        {/*     MIDDLE    */}
        <div className="border border-green-500 h-150 overflow-y-auto">
          {messageList.map((m, i) => {
            return (
              <div
                key={i}
                className={m.role == "user" ? "text-right" : "text-left"}
              >
                {m.text}
              </div>
            );
          })}
        </div>

        {/*     LAST    */}
        <div className="flex justify-between border border-red-500 h-20">
          <form className="flex items-center" onSubmit={handleSubmit}>
            <input
              className="border w-130 h-15"
              type="text"
              placeholder="How may I help you?"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            ></input>
            <button type="submit">
              <IoIosSend size={39} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
