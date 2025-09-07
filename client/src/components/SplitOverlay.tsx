import { useState, useEffect } from "react";
import "./SplitOverlay.css";
import { categories } from "../constants/categories";

interface Person {
    name: string;
    isParticipating: boolean;
    paid: string;
    shouldPay: string;
    percentage: string;
}

interface SplitOverlayProps {
    groupId: number;
    isOpen: boolean;
    onClose: () => void;
    onApply: (data: any) => void;
    token: string;
}

function SplitOverlay({ groupId, isOpen, onClose, onApply, token }: SplitOverlayProps) {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:5000/groups/${groupId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(async (res) => {
            const data = await res.json();
            setUsers(data.users);
        });
    }, [groupId]);

    let peopleList: Person[] = [];

    users.forEach(user => {
        peopleList.push({
            name: user['username'],
            isParticipating: false,
            paid: "0",
            shouldPay: "0",
            percentage: "0",
        });
    });

    const [totalPercentage, setTotalPercentage] = useState(0);
    const [activity, setActivity] = useState("");
    const [totalAmount, setTotalAmount] = useState("");
    const [divideEqually, setDivideEqually] = useState(true);
    const [percentage, setPercentage] = useState(false);
    const [people, setPeople] = useState<Person[]>(peopleList);
    const [totalPaid, setTotalPaid] = useState(0);
    const [isValid, setIsValid] = useState(false);
    const resetOverlay = () => {
        setActivity("");
        setTotalAmount("");
        setDivideEqually(true);
        setPeople(peopleList);
        setTotalPaid(0);
        setIsValid(false);
    };
    const handleParticipantChange = (index: number, checked: boolean) => {
        const newPeople = [...people];
        newPeople[index].isParticipating = checked;
        if (!checked) {
            newPeople[index].paid = "0";
            newPeople[index].shouldPay = "0";
        }
        setPeople(newPeople);
    };
    const handleClose = () => {
        resetOverlay();
        onClose();
    };

    function getSplitType(divideEqually: boolean, percentages: boolean) {
        if (divideEqually) return "divideEqually";
        if (percentages) return "percentages";
        return "individual";
    }

    const handleApply = () => {
        onApply(people);

        fetch(`http://localhost:5000/expense/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                group_id: groupId,
                title: activity,
                amount: Number(totalAmount),
                currency: 'EUR',
                split_type: (getSplitType(divideEqually, percentage)),
                payment_method: '',
                is_paid: false,
                participants: JSON.stringify(peopleList),
                next_payment_date: null,
                expense_type: ''
            })
        })

        onClose();
    };
    useEffect(() => {
        if (divideEqually && totalAmount) {
            const participants = people.filter((p) => p.isParticipating).length;
            const perPerson = participants
                ? (parseFloat(totalAmount) / participants).toFixed(2)
                : "0";
            setPeople(
                people.map((person) => ({
                    ...person,
                    shouldPay: person.isParticipating ? perPerson : "0",
                }))
            );
        }
    }, [
        divideEqually,
        totalAmount,
        people.map((p) => p.isParticipating).join(","),
    ]);

    useEffect(() => {
        if (percentage && totalAmount) {
            setPeople(
                people.map((person) => ({
                    ...person,
                    shouldPay: person.isParticipating
                        ? (
                            (parseFloat(totalAmount) *
                                parseFloat(person.percentage || "0")) /
                            100
                        ).toFixed(2)
                        : "0",
                }))
            );
        }
    }, [
        percentage,
        totalAmount,
        people.map((p) => p.percentage).join(","),
        people.map((p) => p.isParticipating).join(","),
    ]);

    useEffect(() => {
        const total = people
            .filter((p) => p.isParticipating)
            .reduce((sum, person) => sum + parseFloat(person.paid || "0"), 0);
        setTotalPaid(total);
        // Add activity check to validation
        setIsValid(
            total === parseFloat(totalAmount || "0") && total > 0 && activity.trim() !== "" && (totalPercentage <= 100 || !percentage)
        );
    }, [people, totalAmount, activity]); // Add activity to dependencies

    if (!isOpen) return null;

    return (
        <div className="overlay">
            <div className="overlay-content">
                <h2>Split Expense</h2>

                <div className="overlay-header">
                    <div className="input-group">
                        <input
                            type="text"
                            placeholder="Activity (e.g., Pizza)"
                            value={activity}
                            onChange={(e) => setActivity(e.target.value)}
                            className="input"
                        />
                        <input
                            type="number"
                            placeholder="Total Amount"
                            value={totalAmount}
                            onChange={(e) => setTotalAmount(e.target.value)}
                            className="input"
                            min="0"
                        />
                        <select className="input">
                            {categories.slice(1).map((category) => (
                                <option
                                    key={category}
                                    value={category}
                                >
                                    {category}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="checkbox-group">
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={divideEqually}
                                onChange={(e) => {
                                    setDivideEqually(e.target.checked);
                                    if (percentage)
                                        setPercentage(!e.target.checked);
                                }}
                            />
                            Divide Equally
                        </label>
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                checked={percentage}
                                onChange={(e) => {
                                    setPercentage(e.target.checked);
                                    if (divideEqually)
                                        setDivideEqually(!e.target.checked);
                                }}
                            />
                            Percentage
                        </label>
                    </div>
                </div>
                <table className="split-table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Paid</th>
                            <th>Should Pay</th>
                            <th>%</th>
                            <th>Overpaid/Not enough</th>
                        </tr>
                    </thead>
                    <tbody>
                        {people
                            .filter((p) => p)
                            .map((person, index) => (
                                <tr key={index}>
                                    <td className="checkbox-label">
                                        <input
                                            type="checkbox"
                                            checked={person.isParticipating}
                                            onChange={(e) =>
                                                handleParticipantChange(
                                                    index,
                                                    e.target.checked
                                                )
                                            }
                                        />
                                        {person.name}
                                    </td>
                                    <td>
                                        <input
                                            type="number"
                                            value={person.paid}
                                            onChange={(e) => {
                                                const newPeople = [...people];
                                                const personIndex =
                                                    people.findIndex(
                                                        (p) =>
                                                            p.name ===
                                                            person.name
                                                    );
                                                newPeople[personIndex].paid =
                                                    e.target.value;
                                                setPeople(newPeople);
                                            }}
                                            disabled={!person.isParticipating}
                                            className="input"
                                            min="0"
                                        />
                                    </td>
                                    <td>
                                        <input
                                            type="number"
                                            value={person.shouldPay}
                                            onChange={(e) => {
                                                if (!divideEqually) {
                                                    const newPeople = [
                                                        ...people,
                                                    ];
                                                    const personIndex =
                                                        people.findIndex(
                                                            (p) =>
                                                                p.name ===
                                                                person.name
                                                        );
                                                    newPeople[
                                                        personIndex
                                                    ].shouldPay =
                                                        e.target.value;
                                                    setPeople(newPeople);
                                                }
                                            }}
                                            disabled={
                                                divideEqually ||
                                                !person.isParticipating ||
                                                percentage
                                            }
                                            className="input"
                                            max={parseFloat(totalAmount) || 0}
                                            min="0"
                                        />
                                    </td>
                                    <td>
                                        <input
                                            type="number"
                                            value={person.percentage}
                                            onChange={(e) => {
                                                if (percentage) {
                                                    const newPeople = [...people];
                                                    const personIndex = people.findIndex(
                                                        (p) => p.name === person.name
                                                    );
                                                    newPeople[personIndex].percentage = e.target.value;

                                                    // Calculate new total percentage
                                                    const newTotal = newPeople
                                                        .filter(p => p.isParticipating)
                                                        .reduce((sum, p) => sum + parseFloat(p.percentage || "0"), 0);
                                                    setTotalPercentage(newTotal);

                                                    // Update shouldPay based on percentage
                                                    newPeople[personIndex].shouldPay = person.isParticipating
                                                        ? ((parseFloat(totalAmount) * parseFloat(e.target.value)) / 100).toFixed(2)
                                                        : "0";

                                                    setPeople(newPeople);
                                                }
                                            }}
                                            disabled={!percentage || !person.isParticipating}
                                            className="input"
                                            min="0"
                                            max={100}
                                        />
                                    </td>
                                    <td>
                                        <p>
                                            {person.isParticipating
                                                ? `${((person.paid ? parseFloat(person.paid) : 0) - (person.shouldPay ? parseFloat(person.shouldPay) : 0)).toFixed(2)} ${(person.paid ? parseFloat(person.paid) : 0) - parseFloat(person.shouldPay) > 0
                                                    ? "(Overpaid)"
                                                    : (person.paid ? parseFloat(person.paid) : 0) - parseFloat(person.shouldPay) < 0 ? "(Not paid enough)" : "Ok"
                                                }`
                                                : ""}
                                        </p>
                                    </td>
                                </tr>
                            ))}
                        <tr className="total-row">
                            <td>Total</td>
                            <td>${totalPaid.toFixed(2)}</td>
                            <td>${totalAmount || "0"}</td>
                            {percentage && <td>{totalPercentage}%</td>}
                        </tr>
                    </tbody>
                </table>

                <div className="button-group">
                    <button className="primary-btn" onClick={handleClose}>
                        Cancel
                    </button>
                    <button
                        className={`primary-btn ${!isValid ? "disabled" : ""}`}
                        onClick={handleApply}
                        disabled={!isValid}
                    >
                        Apply
                    </button>
                </div>
            </div>
        </div>
    );
}

export default SplitOverlay;
