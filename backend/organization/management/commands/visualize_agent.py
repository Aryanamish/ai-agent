from django.core.management.base import BaseCommand

from organization.agent import app


class Command(BaseCommand):
    help = 'Visualize the LangGraph agent as Mermaid diagram'

    def handle(self, *args, **options):
        try:
            # Get the graph object from the compiled app
            graph = app.get_graph()
            
            # Generate Mermaid syntax
            mermaid_code = graph.draw_mermaid()
            
            output_file = 'agent_graph.mmd'
            
            # Save to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(mermaid_code)
                
            self.stdout.write(mermaid_code)
            self.stdout.write(self.style.SUCCESS(f'\n\nSuccessfully saved mermaid graph to {output_file}'))
            self.stdout.write("You can view this file using a Mermaid viewer or paste the content into https://mermaid.live")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error visualizing graph: {e}'))
