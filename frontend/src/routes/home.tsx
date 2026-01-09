import { createFileRoute } from "@tanstack/react-router";
import { StoreList, type Store } from "@/features/store";

export const Route = createFileRoute("/home")({
  component: HomePage,
});

// Sample store data - replace with actual API data
const sampleStores: Store[] = [
  {
    id: "1",
    name: "Tech Haven",
    description: "Your one-stop shop for all things tech and gadgets.",
    location: "San Francisco, CA",
    image: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400",
  },
  {
    id: "1",
    name: "Tech Haven",
    description: "Your one-stop shop for all things tech and gadgets.",
    location: "San Francisco, CA",
    image: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400",
  },
  {
    id: "1",
    name: "Tech Haven",
    description: "Your one-stop shop for all things tech and gadgets.",
    location: "San Francisco, CA",
    image: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400",
  },
  {
    id: "1",
    name: "Tech Haven",
    description: "Your one-stop shop for all things tech and gadgets.",
    location: "San Francisco, CA",
    image: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400",
  },
  {
    id: "1",
    name: "Tech Haven",
    description: "Your one-stop shop for all things tech and gadgets.",
    location: "San Francisco, CA",
    image: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400",
  },
  {
    id: "1",
    name: "Tech Haven",
    description: "Your one-stop shop for all things tech and gadgets.",
    location: "San Francisco, CA",
    image: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400",
  },
  {
    id: "1",
    name: "Tech Haven",
    description: "Your one-stop shop for all things tech and gadgets.",
    location: "San Francisco, CA",
    image: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400",
  },
  {
    id: "1",
    name: "Tech Haven",
    description: "Your one-stop shop for all things tech and gadgets.",
    location: "San Francisco, CA",
    image: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400",
  },
  {
    id: "2",
    name: "Fashion Forward",
    description: "Trendy clothing and accessories for the modern fashionista.",
    location: "New York, NY",
    image: "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=400",
  },
  {
    id: "3",
    name: "Home Essentials",
    description: "Everything you need to make your house a home.",
    location: "Los Angeles, CA",
    image: "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400",
  },
  {
    id: "4",
    name: "Sports & Outdoors",
    description: "Gear up for your next adventure with our sports equipment.",
    location: "Denver, CO",
    image: "https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=400",
  },
];

export function HomePage() {
  return (

    <div className="py-8 container">
      <h1 className="text-3xl font-bold text-foreground mb-6">Our Stores</h1>
      <StoreList stores={sampleStores} columns={4} />
    </div>
  );
}
