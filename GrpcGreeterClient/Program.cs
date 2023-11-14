using System.Threading.Tasks;
using Grpc.Net.Client;
using GrpcGreeterClient;

// The port number must match the port of the gRPC server.
using var channel = GrpcChannel.ForAddress("http://localhost:5068");
var client = new Greeter.GreeterClient(channel);
var reply = await client.SayHelloAsync(
                  new HelloRequest { Name = "GreeterClient" });
Console.WriteLine("Greeting: " + reply.Message);

int num = 3;

var reply2 = await client.CuadradoAsync(
            new CuadradoRequest { Numero = num});

Console.WriteLine("Cuadrado de " + num + " = " + reply2.Cuadrado);

// Solicitar al usuario que ingrese la patente
Console.Write("Ingrese la patente del automóvil: ");
string patente = Console.ReadLine();

// Mostrar la patente ingresada
Console.WriteLine("La patente ingresada es: " + patente);

// Esperar a que el usuario presione Enter antes de cerrar la aplicación
Console.ReadLine();

Console.WriteLine("Press any key to exit...");
Console.ReadKey();
