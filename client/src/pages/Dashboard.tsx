//React
import { useState, useEffect, useRef } from "react";
//Components
import DebtTable from "../components/DebtTable";
import SplitOverlay from "../components/SplitOverlay";
//Types
import type { Person } from "../types/interfaces";
import type { HistoryActivity } from "../types/interfaces";
//Styles
import "./Dashboard.css";
/*------------------------------------------------------------------------*/
import { Navigate, useFetcher, useNavigate } from "react-router-dom";

interface GroupProps {
    id: number;
    name: string;
    owner_id: number;
}

interface UserProps {
    id: number;
    username: string;
}

function Dashboard() {
    const navigate = useNavigate();

    // Attempt to log in with a JWT token
    const token = localStorage.getItem('jwt');

    useEffect(() => {
        if (!token) navigate('/', { replace: true });
    }, [token, navigate]);

    const hasFetched = useRef(false);

    const [username, setUsername] = useState('');
    useEffect(() => {
        if (hasFetched.current) return;
        hasFetched.current = true;
        
        fetch("http://localhost:5000/user/current_user", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        })
        .then(async (res) => {
            if (res.status == 404) {
                navigate('/', { replace: true });
            } else if (res.status == 500) {
                localStorage.setItem('jwt', '');
                navigate('/', { replace: true });
            } else if (res.status == 200) {
                const result = await res.json();
                console.log("Setting username");
                console.log(result['username']);
                setUsername(result['username']);
                console.log(username);
            } else {
                throw new Error(`Unexpected status: ${res.status}`);
            }
        })
        .catch(err => {
            console.error("Registration error:", err);
            navigate("/signup?error=server", { replace: true });
        });
    }, [token, navigate]);

    const [groupsData, setGroupsData] = useState([]);

    const fetched = useRef(false);

    const [noGroups, setNoGroups] = useState(false);

    useEffect(() => {
        if (fetched.current) return;
        fetched.current = true;

        fetch(`http://localhost:5000/groups/all_user_groups`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(async (res) => {
            const data = await res.json();
            setGroupsData(data['groups']);
            if (!data['groups'] || data['groups'].length === 0) {
                setNoGroups(true);
            }
        })
        .catch(err => {
            console.error(err);
            setNoGroups(true);
        });
    }, [token]);

    const [groupId, setGroupId] = useState(-1);
    const [currentGroup, setCurrentGroup] = useState<GroupProps | null>(null);
    const [groupUsers, setGroupUsers] = useState<UserProps[]>([]);

    const getUsersInGroup = (group: GroupProps) => {
        fetch(`http://localhost:5000/groups/${group.id}`, {
            method: 'GET'
        }).then(async (res) => {
            if (res.status !== 200) {
                console.error(`Wrong status code: ${res.status}`);
                return;
            }

            const data = await res.json();
            console.log(`getUsersInGroup response message for group ${group.id}:`, data.message); // Логируем message
            setGroupUsers(data.users);
        }).catch(err => {
            console.error(`Error fetching users in group ${group.id}:`, err);
        });
    }

    const handleChangeGroup = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const value = event.target.value;

        if (value === 'create') {
            navigate('/create_group', { replace: true });
            return;
        }

        const numericId = Number(value);
        setGroupId(numericId);

        const group = groupsData.find(x => x['id'] === numericId) || null;
        setCurrentGroup(group);

        if (group)
            getUsersInGroup(group!);
    }

    const theyOweList: [] = [

    ];
    const youOweList: [] = [

    ];
    const historyList: [] = [

    ];
    const [theyOwe, setTheyOwe] = useState<Person[]>(theyOweList);
    const [youOwe, setYouOwe] = useState<Person[]>(youOweList);
    const [history, setHistory] = useState<HistoryActivity[]>(historyList);
    const [isOverlayOpen, setIsOverlayOpen] = useState(false);

    const [data, setData] = useState([]);

    const youOweValue = youOweList.reduce((total, currentItem) => { const amount = parseFloat(currentItem.amount.replace('$', '')); return total + amount; }, 0);
    const historyValue = historyList.reduce((total, currentItem) => { const amount = parseFloat(currentItem.amount.replace('$', '')); return total + amount; }, 0)
    const theyOweValue = theyOweList.reduce((total, currentItem) => { const amount = parseFloat(currentItem.amount.replace('$', '')); return total + amount; }, 0);

    const defaultToFirstGroup = () => {
        setGroupId(groupsData[0]['id']) 
    }

    useEffect(() => {
        if (groupsData.length > 0) {
            const firstGroup = groupsData[0];

            setGroupId(firstGroup['id']);
            setCurrentGroup(firstGroup);
            getUsersInGroup(firstGroup);

            fetch(`http://localhost:5000/groups/${firstGroup['id']}`, {
                method: 'GET'
            })
            .then (async (res) => {
                const data = await res.json();
                console.log(`Fetch first group data message for group ${firstGroup.id}:`, data.message); // Логируем message
                setData(data);
            }).catch(err => {
                console.error(`Error fetching first group data for group ${firstGroup.id}:`, err);
            });
        }
    }, [groupsData]);


    // Here we should add the logic for removing one's debt from the server
    const handleDebtResolution = (person: string, reason: string, amount: string) => {
        if (theyOwe.some(debt => debt.person === person)) {
            setTheyOwe(prev => prev.map(debt => 
                debt.person === person ? { ...debt, resolved: true } : debt
            ));
        } else {
            setYouOwe(prev => prev.map(debt => 
                debt.person === person ? { ...debt, resolved: true } : debt
            ));
        }
        // Here you would send the resolution to the server
        // Example:
        // await fetch('/api/resolve-debt', { 
        //     method: 'POST', 
        //     body: JSON.stringify({ person, reason, amount }) 
        // });
    };

    const convertParticipant = (participant: Person) => {
        return JSON.stringify(participant);
    }

    const userId = localStorage.getItem('userid');
    if (!noGroups) {
        return (
        <div className="dashboard">
            {groupId !== -1 ? 
            <div className="dashboard-content">
                <h1 className="small-screen-welcome">
                    Welcome,<br/>
                    <span className="red-text">{username}</span>
                </h1>
                <div className="dashboard-upper">
                    <h1 className="currently-managing-text">
                        Welcome,
                        <span className="red-text"> {username}</span>
                    </h1>
                    <select id="group-select" onChange={handleChangeGroup}>
                        {groupsData.map(x => <option key={x['id']} value={x['id']}>{x['name'] || x['id']}</option>)}
                        <option value='create'>Create new group</option>
                    </select>
                </div>
                <div className="dashboard-header">
                    <div className="dashboard-header-left">
                        <h1 className="dashboard-title">
                            Currently managing: <span className="red-text">{currentGroup!.name}</span>
                        </h1>
                        
                        <div className="add-spending-section">
                            <h1 className="dashboard-title">Add a spending</h1>
                            <button
                                className="primary-btn"
                                onClick={() => setIsOverlayOpen(true)}
                            >
                                +
                            </button>
                        </div>
                    </div>
                    <div className="dashboard-header-right">
                        <button className="primary-btn">Leave</button>
                        <a href={`/invite?id=${groupId}`}>
                            <button className="primary-btn">Add Friend</button>
                        </a>
                    </div>
                </div>
                <div className="table-section table-section-split">
                    <DebtTable
                        title="They Owe You"
                        value={theyOweValue}
                        debts={theyOwe}
                        status="theyOwe"
                        onResolve={handleDebtResolution}
                    />
                    <DebtTable
                        title="You Owe Them"
                        value={youOweValue}
                        debts={youOwe}
                        status="youOwe"
                        onResolve={handleDebtResolution}
                    />
                </div>
                <div className="table-section">
                    <DebtTable
                        title="Group history: spent"
                        value={historyValue}
                        debts={history}
                        status="history"
                    />
                </div>
            </div> : /*<Navigate to="/create_group" replace />*/ <h1>no</h1>}
            <SplitOverlay
                groupId={groupId}
                isOpen={isOverlayOpen}
                onClose={() => setIsOverlayOpen(false)}
                onApply={(data) => {
                    console.log("Split data:", data);
                    setIsOverlayOpen(false);
                }}
                token={token!}
            />
        </div>
    );
}

    return <Navigate to='/create_group' />
}

export default Dashboard;
