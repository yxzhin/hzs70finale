export const categories = ["All", "Food", "Entertainment", "Bills", "Other"] as const;

export type Category = (typeof categories)[number];