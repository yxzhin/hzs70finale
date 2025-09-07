export interface Person {
    person: string;
    reason: string;
    amount: string;
    category: string;
    resolved?: boolean;
}
export interface HistoryActivity {
    reason: string;
    amount: string;
    category: string;
}
