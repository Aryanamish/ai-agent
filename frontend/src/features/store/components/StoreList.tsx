import { StoreCard, type Store } from "./StoreCard";

interface StoreListProps {
  stores: Store[];
  columns?: 2 | 3 | 4;
}

export function StoreList({ stores, columns = 3 }: StoreListProps) {
  const gridColsClass = {
    2: "grid-cols-1 sm:grid-cols-2",
    3: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3",
    4: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4",
  };

  if (stores.length === 0) {
    return (
      <div className="flex items-center justify-center py-12">
        <p className="text-muted-foreground">No stores available</p>
      </div>
    );
  }

  return (
    <div className={`grid gap-6 ${gridColsClass[columns]}`}>
      {stores.map((store) => (
        <StoreCard key={store.id} store={store} />
      ))}
    </div>
  );
}
