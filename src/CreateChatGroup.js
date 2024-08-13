import React, { useState } from 'react';
import myimage from './assets/programmer.png';

export const CreateChatGroup = () => {
  const [groupName, setGroupName] = useState('');
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  const allUsers = [
    { id: 1, name: 'John Doe', role: 'Admin', profileImage: myimage },
    { id: 2, name: 'Jane Smith', role: 'Member', profileImage: myimage },
    { id: 3, name: 'Alice Johnson', role: 'Member', profileImage: myimage },
    // Add more users if needed
  ];

  const filteredUsers = allUsers.filter(
    (user) =>
      user.name.toLowerCase().includes(searchQuery.toLowerCase()) &&
      !selectedUsers.includes(user)
  );

  const handleUserSelection = (user) => {
    if (selectedUsers.includes(user)) {
      setSelectedUsers(selectedUsers.filter((u) => u.id !== user.id));
    } else {
      setSelectedUsers([...selectedUsers, user]);
    }
  };

  return (
    <div className="container">
      <style>
        {`
          .container {
            display: flex;
            flex-direction: row;
            padding: 20px;
            font-family: Arial, sans-serif;
          }
          .groupContainer, .userBox {
            margin: 20px;
            padding: 10px;
            background: darkgrey;
            width: 40%;
            height: 500px;
            position: relative;
            text-align: left;
          }
          .input {
            padding: 10px;
            margin: 10px 0;
            width: 100%;
            box-sizing: border-box;
          }
          .button {
            padding: 10px 20px;
            margin: 10px 5px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
          }
          .cancelButton {
            background-color: #dc3545;
          }
          .userList {
            list-style-type: none;
            padding: 0;
            max-height: 220px;
            overflow-y: auto;
            border-top: 1px solid #ddd;
          }
          .userListItem {
            display: flex;
            align-items: center;
            padding: 10px;
            border-bottom: 5px solid #ddd;
            background: white;
          }
          .userImage {
            border-radius: 50%;
            margin-right: 10px;
          }
          .userName {
            font-weight: bold;
          }
          .userRole {
            margin-left: auto;
            font-style: italic;
            color: #666;
          }
          .bottomRight {
            position: absolute;
            bottom: 10px;
            right: 10px;
          }
          ul::-webkit-scrollbar {
            width: 0.25rem;
          }
          ul::-webkit-scrollbar-track {
            background: #f0f0f0;
          }
          ul::-webkit-scrollbar-thumb {
            background: #888;
          }
        `}
      </style>
      
      <div className="groupContainer">
        <p>Create New Group</p>
        <div>
          <p>Group Name</p>
          <input
            type="text"
            placeholder="Group Name"
            value={groupName}
            onChange={(e) => setGroupName(e.target.value)}
            className="input"
          />
        </div>

        <h4>Selected Users</h4>
        <div>
          <ul className="userList">
            {selectedUsers.map((user) => (
              <li key={user.id} className="userListItem">
                <input
                  type="checkbox"
                  checked
                  onChange={() => handleUserSelection(user)}
                />
                <img
                  src={user.profileImage}
                  alt={`${user.name}'s profile`}
                  width="30"
                  height="30"
                  className="userImage"
                />
                <span className="userName">{user.name}</span>
                <span className="userRole">{user.role}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bottomRight">
          <button className="button cancelButton">Cancel</button>
          <button className="button">Create</button>
        </div>
      </div>

      <div className="userBox">
        <p>Users</p>
        <div>
          <input
            type="text"
            placeholder="Search Users"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input"
          />
        </div>
        <div>
          <ul className="userList">
            {filteredUsers.map((user) => (
              <li key={user.id} className="userListItem">
                <input
                  type="checkbox"
                  checked={selectedUsers.includes(user)}
                  onChange={() => handleUserSelection(user)}
                />
                <img
                  src={user.profileImage}
                  alt={`${user.name}'s profile`}
                  width="30"
                  height="30"
                  className="userImage"
                />
                <span className="userName">{user.name}</span>
                <span className="userRole">{user.role}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
