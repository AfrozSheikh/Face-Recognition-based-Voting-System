// import { useContext } from "react";
// import { AuthContext } from "../context/AuthContext";
// import { useNavigate } from "react-router-dom";

// const Dashboard = () => {
//   const { user, logout } = useContext(AuthContext);
//   const navigate = useNavigate();

//   if (!user || user.role !== "voter") {
//     navigate("/login"); // Redirect to login if not authenticated or not a voter
//     return null;
//   }

//   return (
//     <div>
//       <h2>Welcome, Voter!</h2>
//       <h3>Voter Panel</h3>
//       <ul>
//         <li>
//           <button onClick={() => navigate("/voter/elections")}>
//             View Elections
//           </button>
//         </li>
//         <li>
//           <button onClick={() => navigate("/voter/vote")}>Cast Vote</button>
//         </li>
//       </ul>

//       <button
//         onClick={() => {
//           logout();
//           navigate("/login");
//         }}
//       >
//         Logout
//       </button>
//     </div>
//   );
// };

// export default Dashboard;

import { useContext, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const { role, logout ,user} = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
   
    
    
    if (!role || role !== "voter") {
      navigate("/login"); // Redirect only after initial render
    }
  }, [role, navigate]);

  // if (!user || user.role !== "voter") {
  //   return null; // Avoid rendering anything before redirection
  // }

  return (
    <div>
      <h2>Welcome, Voter!</h2>
      <h3>Voter Panel</h3>
      <ul>
        <li>
          <button onClick={() => navigate("/view-elections")}>
            View Elections
          </button>
        </li>
        <li>
          <button onClick={() => navigate("/results")}>
            Result
          </button>
        </li>


        <li>
          <button onClick={() => navigate("/vote")}>Cast Vote</button>
        </li>
      </ul>

      <button
        onClick={() => {
          logout();
          navigate("/login");
        }}
      >
        Logout
      </button>
    </div>
  );
};

export default Dashboard;
