import "./Dashboard.css";
import DebtItem from "../components/DebtItem";
import SplitOverlay from "../components/SplitOverlay";
import { useEffect, useRef, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";

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
                setUsername(result['username']);
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
            setGroupUsers(data.users);
        })
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

    const [isOverlayOpen, setIsOverlayOpen] = useState(false);
    let theyOweValue = "$40.00";
    let youOweValue = "$17.50";
    let historyValue = "$40.00";

    const defaultToFirstGroup = () => {
        setGroupId(groupsData[0]['id'])
    }

    useEffect(() => {
    if (groupsData.length > 0) {
        setGroupId(groupsData[0]['id']);
        setCurrentGroup(groupsData[0]);
        getUsersInGroup(groupsData[0]);
    }
}, [groupsData]);

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
                    <div className="they-owe">
                        <h2 className="table-title">
                            They Owe You {theyOweValue}
                        </h2>
                        <div className="debt-list">
                            <DebtItem
                                person="John Doe"
                                reason="Pizza"
                                amount="$15.00"
                                status="theyOwe"
                            />
                            <DebtItem
                                person="Alice Smith"
                                reason="Movie tickets"
                                amount="$25.00"
                                status="theyOwe"
                            />
                        </div>
                    </div>

                    <div className="you-owe">
                        <h2 className="table-title">
                            You Owe Them {youOweValue}
                        </h2>
                        <div className="debt-list">
                            <DebtItem
                                person="Bob Johnson"
                                reason="Lunch"
                                amount="$12.50"
                                status="youOwe"
                            />
                            <DebtItem
                                person="Sarah Wilson"
                                reason="Coffee"
                                amount="$5.00"
                                status="youOwe"
                            />
                        </div>
                    </div>
                </div>
                <div className="table-section">
                    <div className="history">
                        <h2 className="table-title">
                            Group history: spent {historyValue} together
                        </h2>
                        <div className="debt-list">
                            <DebtItem
                                person="John Doe"
                                reason="Pizza"
                                amount="$15.00"
                                status="history"
                            />
                            <DebtItem
                                person="Alice Smith"
                                reason="Movie tickets"
                                amount="$25.00"
                                status="history"
                            />
                        </div>
                    </div>
                </div>
            </div> : /*<Navigate to="/create_group" replace />*/ <h1>no</h1>}
            <SplitOverlay
                isOpen={isOverlayOpen}
                onClose={() => setIsOverlayOpen(false)}
                onApply={(data) => {
                    console.log("Split data:", data);
                    setIsOverlayOpen(false);
                    // Here you would handle the split data
                }}
            />
        </div>
    );
}

    return <Navigate to='/create_group' />
}

export default Dashboard;
