import {  Link } from "react-router";
import { useEffect, useState } from "react";
import API from "@/lib/Axios";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { OrgDetails } from "@/routes";





export function HomePage({orgs}: {orgs: OrgDetails[] | null}) {

  return (

    <div className="py-8 container px-4">
      <h1 className="text-3xl font-bold text-foreground mb-6">Our Stores</h1>
      <div className="flex w-full gap-10">


        {orgs?.map((org) => {
          return <Link to={`/${org.name}/chat`} key={org.id}>
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
