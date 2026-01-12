import {  Link } from "react-router";
import {useLoaderData} from "react-router";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { OrgDetails } from "@/routes";





export function HomePage() {
  const data = useLoaderData().data as OrgDetails[];
  return (

    <div className="py-8 container px-4">
      <h1 className="text-3xl font-bold text-foreground mb-6">Our Stores</h1>
      <div className="flex w-full gap-10">


        {data?.map((org) => {
          return <Link to={`/${org.slug}/chat`} key={org.id}>
            <Card className="cursor-pointer transition-all duration-200 hover:ring-2 hover:ring-primary hover:shadow-lg w-40">
              <CardHeader>
                <CardTitle>

                  {org.name}
                </CardTitle>
                <CardDescription>
                  {org.domain}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground text-sm line-clamp-2">
                  {org.address}
                </p>
              </CardContent>
            </Card>
          </Link>

        })}
      </div>
    </div>
  );
}
