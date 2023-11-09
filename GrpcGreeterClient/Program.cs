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


Console.WriteLine("Press any key to exit...");
Console.ReadKey();
