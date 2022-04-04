#pragma once

#include <cstdint>
#include <cstddef>
#include <unordered_map>
#include <vector>
#include <string>
#include <atomic>
#include <grpcpp/grpcpp.h>

#include <send_array.grpc.pb.h>

#include <types_lookup.hpp>


namespace send_array {

template<typename GrpcType>
class ServiceImpl final: public GrpcType::Service {
    private:
        using data_type = typename TypesLookup<GrpcType>::data_type;
        using single_message_type = typename TypesLookup<GrpcType>::single_message_type;
        using repeated_message_type = typename TypesLookup<GrpcType>::repeated_message_type;

        std::unordered_map<array_id_type, std::vector<data_type>> data__;
        std::atomic<array_id_type> id_counter__;

    public:
        ServiceImpl(): data__(), id_counter__(0) {}

        grpc::Status PostArray(
            grpc::ServerContext* context,
            const repeated_message_type* request,
            ArrayID *response
        ) override {
            auto id = id_counter__++;
            response->set_value(id);
            data__.emplace(id, std::vector<data_type>(request->payload().cbegin(), request->payload().cend()));
            return grpc::Status::OK;
        }

        grpc::Status DeleteArray(
            grpc::ServerContext* context,
            const ArrayID* request,
            Empty* response
        ) override {
            data__.erase(request->value());
            return grpc::Status::OK;
        }

        grpc::Status GetArray(
            grpc::ServerContext* context,
            const ArrayID* request,
            repeated_message_type* response
        ) override {
            const auto & source_vec = data__.at(request->value());
            response->mutable_payload()->Add(
                source_vec.cbegin(),
                source_vec.cend()
            );
            return grpc::Status::OK;
        }

        grpc::Status GetArrayStreaming(
            grpc::ServerContext* context,
            const ArrayID* request,
            grpc::ServerWriter<single_message_type>* writer
        ) override {
            const auto & source_vec = data__.at(request->value());

            single_message_type message;
            for(auto item: source_vec) {
                message.set_payload(item);
                writer->Write(message);
            }
            return grpc::Status::OK;
        }

        grpc::Status GetArrayChunked(
            grpc::ServerContext* context,
            const StreamRequest* request,
            grpc::ServerWriter<repeated_message_type>* writer
        ) override {
            auto chunk_size = request->chunk_size();
            repeated_message_type chunk;
            const auto & source_vec = data__.at(request->array_id().value());
            for(
                auto it=source_vec.cbegin();
                it < source_vec.cend();
                std::advance(it, chunk_size)
            ) {
                chunk.mutable_payload()->Clear();
                chunk.mutable_payload()->Add(it, std::min(it + chunk_size, source_vec.cend()));
                writer->Write(chunk);
            }
            return grpc::Status::OK;
        }

        grpc::Status GetArrayBinaryChunked(
            grpc::ServerContext* context,
            const StreamRequest* request,
            grpc::ServerWriter<BinaryChunk>* writer
        ) override {
            auto chunk_size = request->chunk_size();

            const auto & source_vec = data__.at(request->array_id().value());
            auto ptr = reinterpret_cast<const char*>(&source_vec.front());
            const auto end = reinterpret_cast<const char* const>(&source_vec.back() + 1);

            BinaryChunk chunk;
            // Add chunks that can be transmitted fully
            while(ptr < end - chunk_size) {
                chunk.set_payload(ptr, chunk_size);
                writer -> Write(chunk);
                ptr += chunk_size;
            }
            // Add last partial chunk
            chunk.set_payload(ptr, (end - ptr));
            writer-> Write(chunk);

            return grpc::Status::OK;
        }
};

} // end namespace send_array
