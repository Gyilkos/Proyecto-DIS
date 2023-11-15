using Grpc.Core;
using servicio;

namespace servicio.Services;

public class GreeterService : Greeter.GreeterBase
{
    private readonly ILogger<GreeterService> _logger;
    public GreeterService(ILogger<GreeterService> logger)
    {
        _logger = logger;
    }

    public override Task<HelloReply> SayHello(HelloRequest request, ServerCallContext context)
    {
        return Task.FromResult(new HelloReply
        {
            Message = "Hello " + request.Name
        });
    }

    public override Task<CuadradoReply> Cuadrado(CuadradoRequest request, ServerCallContext context)
    {
        return Task.FromResult(new CuadradoReply { Cuadrado = request.Numero*request.Numero});
    }


    // public override Task<PatenteReply> Patente(PatenteRequest request, ServerCallContext context)
    // {
    //     // Supongamos que esta función busca el estado de la patente
    //     string estadoPatente = BuscarEstadoPatente(request.NumeroPatente);

    //     return Task.FromResult(new PatenteReply { EstadoPatente = estadoPatente });
    // }
}
