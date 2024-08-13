import React, { useRef, useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import myImage from './assets/programmer.png';

function ChatRoom() {
  const [formValue, setFormValue] = useState('');
  const [messages, setMessages] = useState([]);
  const [socket, setSocket] = useState(null);
  const [groups, setGroups] = useState([]); // To store group names
  const [selectedGroup, setSelectedGroup] = useState(''); // Track the selected group ID
  const [joinedGroupId, setJoinedGroupId] = useState(0); // Track the joined group ID
  const [error, setError] = useState('');
  const dummy = useRef();

  const SOCKET_URL = `ws://localhost:8000/api/v1/chat/message`;
  const CHAT_HISTORY_URL = `http://localhost:8000/api/v1/chat/load_messages`;
  const GROUPS_URL = `http://localhost:8000/api/v1/chat/groups`; // URL to fetch groups

  const location = useLocation();
  const clientid = location.state.client_id;

  useEffect(() => {
    // Fetch the available groups when the component mounts
    const fetchGroups = async () => {
      try {
        const response = await fetch(GROUPS_URL);
        const data = await response.json();
        console.log('Fetched groups:', data);
        if (Array.isArray(data)) {
          setGroups(data);
          console.log(groups)
        } else {
          console.error('Unexpected data format:', data);
          setGroups([]);
        }
      } catch (error) {
        console.error('Failed to load groups:', error);
        setGroups([]);
      }
    };

    fetchGroups();
  }, []);

  const fetchChatHistory = async (groupId) => {
    try {
      const response = await fetch(`${CHAT_HISTORY_URL}/${groupId}`);
      const data = await response.json();
      const previousMessages = data.map((message) =>
        loadPreviousMessages({ data: message, client_id: clientid })
      );
      setMessages(previousMessages);
    } catch (error) {
      console.error('Failed to load chat history:', error);
    }
  };

  const handleJoin = async (groupId) => {
    // Ensure groupId is a number
    const numericGroupId = Number(groupId);
    if (numericGroupId === joinedGroupId) {
      setError('You have already joined this chat.');
      return;
    }
  
    try {
      if (socket) {
        // Close the previous WebSocket connection before establishing a new one
        socket.close();
      }
  
      await fetchChatHistory(numericGroupId);
  
      const ws = new WebSocket(`${SOCKET_URL}/${numericGroupId}`);
  
      ws.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data);
          const message = JSON.parse(parsed.message);
          setMessages((prevMessages) => [
            ...prevMessages,
            { ...message, type: 'received' },
          ]);
        } catch (error) {
          console.error('JSON parse error:', error);
        }
      };
  
      setSocket(ws);
      setJoinedGroupId(numericGroupId); // Update the joined group ID with the numeric value
      setError(''); // Clear any previous error messages
    } catch (error) {
      console.error('Failed to join chat:', error);
      setError('Failed to join the chat.');
    }
  };
    console.log(joinedGroupId)

  const sendMessage = (e) => {
    e.preventDefault();
    console.log(1)
    if (socket && formValue.trim()) {
      console.log(2)
      const message = {
        client_id: clientid,
        text: formValue,
        type: 'sent',
        groupId: selectedGroup,
      };
      console.log(3)
      socket.send(JSON.stringify(message));
      setMessages((prevMessages) => [...prevMessages, message]);
      console.log(4)
      setFormValue('');
      dummy.current.scrollIntoView({ behavior: 'smooth' });
      console.log(5)
    }
  };

  const loadPreviousMessages = ({ data, client_id }) => {
    const type = data.sender_id === client_id ? 'sent' : 'received';
    return {
      text: data.content,
      type: type,
    };
  };

  return (
    <>
      <style>
        {`
          body {
            background-color: #f0f0f0;
            color: #000;
            font-family: Arial, sans-serif;
          }

          .App {
            text-align: center;
            max-width: 728px;
            margin: 0 auto;
            padding-top: 10px;
          }

          .App header {
            background-color: black;
            height: 10vh;
            min-height: 50px;
            color: white;
            position: fixed;
            width: 55%;
            top: 0px;
            display: flex;
            align-items: center;
            z-index: 99;
            padding: 10px;
            box-sizing: border-box;
            margin-left: 284px;
          }

          .chat-header {
            background-color: #181717;
            color: white;
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #ddd;
          }

          .container {
            display: flex;
            flex-direction: column;
            margin-left: 274px;
          }

          .chat-id {
            position: fixed;
            left: 0;
            width: 43%;
            background-color: #fff;
            border-bottom: 1px solid #ddd;
            display: flex;
            align-items: center;
            padding: 3px;
          }

          .chat-id select {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-right: 10px;
          }

          .chat-id button {
            padding: 10px 20px;
            border: none;
            background-color: #28a745;
            color: white;
            border-radius: 5px;
            cursor: pointer;
          }

          .chat-id button:disabled {
            background-color: #aaa;
            cursor: not-allowed;
          }

          main {
            margin-top: 55px;
            padding: 10px;
            height: calc(100vh - 80px - 50px);
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            background-color: #fff;
          }

          main::-webkit-scrollbar {
            width: 0.25rem;
          }

          main::-webkit-scrollbar-track {
            background: #f0f0f0;
          }

          main::-webkit-scrollbar-thumb {
            background: #888;
          }

          form {
            height: 50px;
            position: fixed;
            bottom: 0;
            background-color: #181717;
            width: 100%;
            max-width: 728px;
            display: flex;
            font-size: 1rem;
            padding: 10px;
            box-sizing: border-box;
          }

          form button {
            width: 20%;
            background-color: #6658b8;
            border: none;
            color: white;
            cursor: pointer;
            transition: background-color 0.3s ease;
            border-radius: 0 5px 5px 0;
          }

          form button:hover {
            background-color: #52459d;
          }

          form input {
            line-height: 1.5;
            width: 80%;
            font-size: 1rem;
            background: #3a3a3a;
            color: white;
            outline: none;
            border: none;
            padding: 0 10px;
            border-radius: 5px 0 0 5px;
          }

          button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
          }

          ul, li {
            list-style: none;
            padding: 0;
            margin: 0;
          }

          .message {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            width: 100%;
            color: #000;
            line-break: anywhere;
            text-align: left;
          }

          .message img {
            border-radius: 50%;
            margin-right: 10px;
            width: 40px;
            height: 40px;
          }

          .message p {
            background: #444;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin: 0;
          }

          .sent {
            flex-direction: row-reverse;
          }

          .sent p { 
            color: white;
            background: #0b93f6;
            align-self: flex-end;
          }

          .received p {
            background: #e5e5ea;
            color: black;
            line-break: anywhere;
            text-align: left;
          }
          img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin: 2px 5px;
          }
          .warning {
            color: red; 
          }
        `}
      </style>
      <header className="chat-header">
        Chat Room
      </header>
      <div className="container">
        <div className="chat-id">
        <select
          value={selectedGroup}
          onChange={(e) => setSelectedGroup(e.target.value)}
          >
          <option value="" disabled>Select a group</option>
          {Array.isArray(groups) && groups.map((group) => (
          <option key={group.id} value={group.id}>
          {group.group_name}
          </option>
        ))}
</select>
          <div className='warning'>
            <p>{error}</p>
          </div>
          <button
            type="button"
            onClick={() => handleJoin(selectedGroup)}
            disabled={!selectedGroup}
          >
            Join
          </button>
        </div>
        <main>
          {messages.map((msg, index) => (
            <ChatMessage key={index} message={msg} />
          ))}
          <span ref={dummy}></span>
        </main>
        {selectedGroup && (
          <form onSubmit={sendMessage}>
            <input
              value={formValue}
              onChange={(e) => setFormValue(e.target.value)}
              placeholder="Say something nice"
            />
            <button type="submit" disabled={!formValue} >
              Send
            </button>
          </form>
        )}
      </div>
    </>
  );
}

function ChatMessage({ message }) {
  const { text, type } = message;
  const messageClass = type === 'sent' ? 'message sent' : 'message received';

  return (
    <div className={messageClass}>
      <img src={myImage} alt="Avatar" />
      <p>{text}</p>
    </div>
  );
}

export default ChatRoom;
