import { Link } from "@tanstack/react-router";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export interface Store {
  id: string;
  name: string;
  description?: string;
  image?: string;
  location?: string;
}

interface StoreCardProps {
  store: Store;
}

export function StoreCard({ store }: StoreCardProps) {
  return (
    <Link to="/$storeName/chat" params={{ storeName: store.name }}>
      <Card className="cursor-pointer transition-all duration-200 hover:ring-2 hover:ring-primary hover:shadow-lg">
        {store.image && (
          <img
            src={store.image}
            alt={store.name}
            className="w-full h-40 object-cover"
          />
        )}
        <CardHeader>
          <CardTitle className="text-base">{store.name}</CardTitle>
          {store.location && (
            <CardDescription>{store.location}</CardDescription>
          )}
        </CardHeader>
        {store.description && (
          <CardContent>
            <p className="text-muted-foreground text-sm line-clamp-2">
              {store.description}
            </p>
          </CardContent>
        )}
      </Card>
    </Link>
  );
}
