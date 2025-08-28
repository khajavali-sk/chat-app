import React from "react";
import { Users, Shield, Wifi } from "lucide-react";

const UserList = ({ users, onUserClick, isConnected }) => {
  return (
    <div className="bg-slate-800/80 backdrop-blur-sm rounded-xl p-4 sm:p-6 border border-slate-700/50 shadow-lg h-full flex flex-col max-h-full">
      <div className="flex items-center justify-between mb-4 sm:mb-6">
        <h2 className="text-lg sm:text-xl font-bold flex items-center space-x-2 text-white">
          <Users className="w-5 h-5 text-emerald-400" />
          <span>Online Users</span>
        </h2>
        <div className="flex items-center space-x-2 bg-slate-700/50 px-2 px-3 py-1 rounded-full">
          <div
            className={`w-3 h-3 rounded-full ${
              isConnected ? "bg-emerald-500 animate-pulse" : "bg-rose-500"
            }`}
          ></div>
          <span className="text-xs sm:text-sm text-slate-300">
            {isConnected ? "Connected" : "Disconnected"}
          </span>
        </div>
      </div>

      {users.length === 0 ? (
        <div className="text-center py-8 sm:py-10 bg-slate-700/30 rounded-xl flex justify-center border border-slate-600/20">
          <div>
            <div className="bg-slate-700/70 p-4 rounded-full inline-block mb-4 shadow-inner border border-slate-600/30">
              <Wifi className="w-10 sm:w-12 h-10 sm:h-12 text-slate-400 mx-auto" />
            </div>
            <p className="text-slate-300 font-medium">No other users online</p>
            <p className="text-sm text-slate-400 mt-2">
              Waiting for others to join...
            </p>
          </div>
        </div>
      ) : (
        <div className="space-y-3 flex-1 overflow-y-auto pr-2 custom-scrollbar">
          {users.map((user) => (
            <div
              key={user.id}
              className="flex-row items-center justify-between p-3 sm:p-3.5 bg-slate-700/50 rounded-xl hover:bg-slate-700/80 transition-all duration-200 cursor-pointer border border-slate-600/30 hover:border-emerald-500/30 shadow-sm hover:shadow w-full"
              onClick={() => onUserClick(user)}
            >
              <div className="flex items-center space-x-3 min-w-0 flex-1">
                <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-violet-500 to-purple-600 rounded-full flex items-center justify-center shadow-md flex-shrink-0 border-2 border-purple-400/30">
                  <span className="text-white font-semibold text-base sm:text-lg">
                    {user.display_name.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div className="min-w-0 flex-1">
                  <div className="font-medium text-white truncate">
                    {user.display_name}
                  </div>
                  <div className="text-xs sm:text-sm text-slate-300 flex items-center space-x-2 mt-0.5">
                    <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                    <span>Online</span>
                  </div>
                </div>
              </div>
              <button
                className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-3 sm:px-4 py-2 mt-1 rounded-lg transition-all duration-200 shadow hover:shadow-md text-xs sm:text-sm flex items-center space-x-1 sm:space-x-2 flex-shrink-0"
                onClick={(e) => {
                  e.stopPropagation();
                  onUserClick(user);
                }}
              >
                <Shield className="w-3 sm:w-3.5 h-3 sm:h-3.5" />
                <span className="hidden sm:inline">Secure Chat</span>
                <span className="sm:hidden">Chat</span>
              </button>
            </div>
          ))}
        </div>
      )}

      <div className="mt-4 sm:mt-6 p-4 sm:p-5 bg-gradient-to-b from-slate-700/50 to-slate-800/50 rounded-xl border border-slate-600/30 shadow-md hover:border-emerald-500/30 transition-all duration-300">
        <div className="flex items-center space-x-2 mb-2">
          <Shield className="w-5 h-5 text-emerald-400" />
          <span className="text-sm font-medium text-white">
            Quantum Security
          </span>
        </div>
        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
          All conversations are secured using quantum key distribution (BB84
          protocol) with automatic eavesdropper detection.
        </p>
      </div>
    </div>
  );
};

export default UserList;
