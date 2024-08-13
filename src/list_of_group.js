import React from 'react'
import image from './assets/programmer.png'

export const list_of_group  = () => {
  return (
    <div>
      
      <ul className="userList">
            {selectedUsers.map((user) => (
              <li key={user.id} className="userListItem">
                
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
  )
}
